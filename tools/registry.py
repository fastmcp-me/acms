"""
Tool registry for discovering and loading ACMS MCP tools.
"""
import importlib
import pkgutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger("ACMS")

TOOL_CATEGORIES = [
    "container",
    "image",
    "network",
    "volume",
    "builder",
    "auth",
    "system",
]


class ToolRegistry:
    """Registry for managing MCP tool discovery and loading."""

    def __init__(self):
        self._tools: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict] = {}

    def discover_tools(self, categories: Optional[List[str]] = None) -> List[str]:
        """
        Discover all available tools in specified categories.

        Args:
            categories: List of category names to search, or None for all

        Returns:
            List of tool names in format 'category.tool_name'
        """
        categories = categories or TOOL_CATEGORIES
        discovered = []

        for category in categories:
            category_path = Path(__file__).parent / category
            if not category_path.exists():
                logger.warning(f"Category directory not found: {category}")
                continue

            for module_info in pkgutil.iter_modules([str(category_path)]):
                if module_info.name.startswith("_"):
                    continue
                tool_name = f"{category}.{module_info.name}"
                discovered.append(tool_name)

        logger.info(f"Discovered {len(discovered)} tools across {len(categories)} categories")
        return discovered

    def load_tool(self, tool_name: str) -> Any:
        """
        Load a single tool by name.

        Args:
            tool_name: Tool name in format 'category.tool_name' (e.g., 'container.list')

        Returns:
            The loaded module

        Raises:
            ImportError: If the tool module cannot be loaded
        """
        if tool_name in self._tools:
            return self._tools[tool_name]

        category, name = tool_name.split(".", 1)
        module_path = f"tools.{category}.{name}"

        try:
            module = importlib.import_module(module_path)
            self._tools[tool_name] = module

            if hasattr(module, "TOOL_METADATA"):
                self._metadata[tool_name] = module.TOOL_METADATA

            logger.debug(f"Loaded tool: {tool_name}")
            return module
        except ImportError as e:
            logger.error(f"Failed to load tool {tool_name}: {e}")
            raise

    def register_all(self, mcp) -> int:
        """
        Register all discovered tools with the MCP server.

        Args:
            mcp: FastMCP server instance

        Returns:
            Number of tools registered
        """
        tools = self.discover_tools()
        count = 0

        for tool_name in tools:
            try:
                module = self.load_tool(tool_name)
                if hasattr(module, "register"):
                    module.register(mcp)
                    count += 1
                else:
                    logger.warning(f"Tool {tool_name} has no register function")
            except Exception as e:
                logger.error(f"Failed to register tool {tool_name}: {e}")

        logger.info(f"Registered {count} tools with MCP server")
        return count

    def register_category(self, mcp, category: str) -> int:
        """
        Register all tools in a specific category.

        Args:
            mcp: FastMCP server instance
            category: Category name

        Returns:
            Number of tools registered
        """
        tools = self.discover_tools([category])
        count = 0

        for tool_name in tools:
            try:
                module = self.load_tool(tool_name)
                if hasattr(module, "register"):
                    module.register(mcp)
                    count += 1
            except Exception as e:
                logger.error(f"Failed to register tool {tool_name}: {e}")

        return count

    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        """
        Search tools by keyword for progressive discovery.

        Args:
            query: Search query string

        Returns:
            List of matching tool metadata
        """
        # Ensure all tools are loaded for searching
        if not self._metadata:
            for tool_name in self.discover_tools():
                try:
                    self.load_tool(tool_name)
                except Exception:
                    pass

        results = []
        query_lower = query.lower()

        for tool_name, metadata in self._metadata.items():
            keywords = metadata.get("keywords", [])
            description = metadata.get("description", "")
            name = metadata.get("name", tool_name)

            if (
                query_lower in description.lower()
                or query_lower in name.lower()
                or any(query_lower in kw.lower() for kw in keywords)
            ):
                results.append({"name": tool_name, "metadata": metadata})

        return results

    def get_tool_metadata(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific tool.

        Args:
            tool_name: Tool name in format 'category.tool_name'

        Returns:
            Tool metadata dictionary or None
        """
        if tool_name not in self._metadata:
            try:
                self.load_tool(tool_name)
            except Exception:
                return None

        return self._metadata.get(tool_name)

    def list_categories(self) -> List[Dict[str, Any]]:
        """
        List all available categories with tool counts.

        Returns:
            List of category information
        """
        categories = []
        for category in TOOL_CATEGORIES:
            tools = self.discover_tools([category])
            categories.append(
                {
                    "name": category,
                    "tool_count": len(tools),
                    "tools": [t.split(".", 1)[1] for t in tools],
                }
            )
        return categories


# Global registry instance
registry = ToolRegistry()
