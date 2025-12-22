# ACMS End-to-End Test Guide for Claude

## Overview
This guide provides Claude with instructions to perform comprehensive end-to-end testing of all ACMS tool functions. Use this when you need to validate ACMS functionality or verify system status.

## Test Execution Instructions

### Prerequisites
- Ensure you're connected to acms via `/mcp` command
- acms should be running
- Use TodoWrite tool to track progress through all test categories

### Test Categories (Execute in Order)

#### 1. System Status and Basic Info
```
mcp__acms__system_status
mcp__acms__container_list (with all=true)
mcp__acms__image_list
```
**Expected**: System running, current containers/images listed

#### 2. Image Operations
```
mcp__acms__image_pull (test with: redis or nginx or postgres)
mcp__acms__image_inspect (inspect the pulled image)
mcp__acms__image_tag (tag the image with a test name)
mcp__acms__image_delete (delete the tagged image using array parameter)
mcp__acms__image_prune

# CLEANUP: Delete the base pulled image
mcp__acms__image_delete (delete the original pulled image, e.g., ["redis:latest"])
```
**Critical Test**: Verify `image_delete` works with array parameter like `["image:tag"]`
**Cleanup**: Ensure both the tagged test image AND the original pulled image are removed

#### 3. Container Lifecycle
```
mcp__acms__container_create (create from pulled image)
mcp__acms__container_run (run detached container)
mcp__acms__container_start (start the created container)
mcp__acms__container_list (verify states)
mcp__acms__container_stop (stop specific containers using array parameter)
mcp__acms__container_kill (kill specific containers using array parameter)
mcp__acms__container_delete (delete specific containers using array parameter)
```
**Critical Test**: Verify individual container targeting works with arrays

#### 4. Container Interaction and Monitoring
```
mcp__acms__container_run (create a long-running container like nginx, save container name/ID)
mcp__acms__container_logs (get container logs)
mcp__acms__container_inspect (get detailed container info)
mcp__acms__container_stats (monitor resource usage - CPU, memory, I/O)
mcp__acms__container_exec (execute command like "nginx -v" or "ls /etc")

# CLEANUP: Remove the test container
mcp__acms__container_stop (stop the nginx container using array parameter)
mcp__acms__container_delete (delete the nginx container using array parameter)
```
**Critical Test**: Container exec should work with service containers (nginx, not alpine)
**New**: `container_stats` provides real-time resource consumption metrics with --no-stream for single snapshot
**Cleanup**: Always stop and delete containers created during this test category

#### 5. Network Operations
```
mcp__acms__network_list
mcp__acms__network_create (create test network)
mcp__acms__network_inspect (inspect created network)
mcp__acms__network_delete (delete specific network using array parameter)
```
**Critical Test**: Verify `network_delete` works with array parameter like `["network-name"]`

#### 6. Volume Operations
```
mcp__acms__volume_list
mcp__acms__volume_create (create test volume with size)
mcp__acms__volume_inspect (inspect created volume)
mcp__acms__volume_delete (delete by name using array parameter)
mcp__acms__volume_prune (remove unreferenced volumes)
```
**Expected**: Volume operations should always work (historically reliable)
**New**: `volume_prune` removes volumes not referenced by any containers

#### 7. Builder Operations
```
mcp__acms__builder_status
mcp__acms__builder_start
mcp__acms__builder_status (confirm running)
mcp__acms__builder_stop
mcp__acms__builder_delete
```

#### 8. System Operations
```
mcp__acms__system_logs (with last="30s" or similar)
mcp__acms__system_df (disk usage by resource type - images, containers, volumes)
mcp__acms__system_dns_list

# Property testing with cleanup safeguards
mcp__acms__system_property_list (list all system properties)
mcp__acms__system_property_get (get a test property value, save original if exists)
mcp__acms__system_property_set (set a test property value, use non-critical property)

# CLEANUP: Restore original state
mcp__acms__system_property_clear (clear the test property if it was originally unset)
# OR
mcp__acms__system_property_set (restore original value if it was previously set)
```
**Note**: System property operations allow reading and managing container system configuration properties
**New**: `system_df` reports disk space usage broken down by images, containers, volumes, and build cache
**Cleanup**: Always restore original property values or clear test properties. NEVER modify critical properties like `build.rosetta`
**Safe Test Properties**: Use properties that don't affect system operation (avoid kernel, rosetta, critical paths)

### Key Testing Principles

#### Cleanup Requirements (CRITICAL)
**All tests must clean up after themselves to prevent resource accumulation and system pollution.**

Cleanup checklist for each test category:
- ✅ **Images**: Delete ALL pulled/created images (both tagged and original)
- ✅ **Containers**: Stop and delete ALL created containers
- ✅ **Networks**: Delete ALL created test networks
- ✅ **Volumes**: Delete ALL created test volumes (prune will handle the rest)
- ✅ **System Properties**: Restore original values or clear test properties
- ✅ **Builder**: Delete builder if created during testing

**Post-Test Verification**:
After completing all test categories, verify clean state:
```
mcp__acms__container_list (should show minimal/no test containers)
mcp__acms__image_list (should show minimal/no test images)
mcp__acms__network_list (should show only default network)
mcp__acms__volume_list (should show minimal/no test volumes)
mcp__acms__system_df (verify disk usage is reasonable)
```

**Emergency Cleanup Commands** (if tests are interrupted):
```
mcp__acms__container_stop_all (stop all running containers)
mcp__acms__container_delete_all (delete all containers)
mcp__acms__image_prune (remove dangling images)
mcp__acms__volume_prune (remove unreferenced volumes)
```

#### Array Parameter Validation (CRITICAL)
The most important test is verifying these functions work with array parameters:
- `image_delete(images=["image1:tag", "image2:tag"])`
- `container_stop(containers=["container1", "container2"])`
- `container_kill(containers=["container1"])`
- `container_delete(containers=["container1", "container2"])`
- `network_delete(networks=["network1"])`

#### Container Exec Requirements
- Use **service containers** (nginx, apache) not utility containers (alpine, busybox)
- Service containers maintain running state and have proper PATH configuration
- Test commands: `nginx -v`, `nginx -t`, `ls /etc/nginx`

#### Expected Success Patterns
- **100% Success Rate**: All functions should work (as of Session 5)
- **Individual Targeting**: Array parameters should work for all delete/stop/kill operations
- **Bulk Operations**: `--all` flags should work as fallback
- **Container Persistence**: Containers may persist across test sessions

### Error Patterns to Watch For

#### Previous Issues (Should be RESOLVED)
```
Error: Input validation error: '["item-name"]' is not valid under any of the given schemas
```
**If you see this**: The array parameter validation issues have returned

#### Expected Errors (Normal Behavior)
None

### Test Execution Template

```markdown
# ACMS Comprehensive End-to-End Test Results

## Test Summary
**Date**: [DATE]
**Success Rate**: X/56 functions (Y%)
**Status**: [BREAKTHROUGH/REGRESSION/STABLE]
**ACMS Version**: 0.0.9+ (with latest CLI updates)

## System Environment
- **Container CLI Version**: [from system_version]
- **ACMS Build**: [from system_status]
- **Images Available**: [count from image_list]
- **Running Containers**: [count from container_list]
- **Disk Usage**: [from system_df]

## Results by Category
### ✅ System Status: [X/4 functions] (+1: system_version)
### ✅ Image Operations: [X/5 functions]
### ✅ Container Lifecycle: [X/7 functions]
### ✅ Container Interaction: [X/5 functions] (+1: container_stats)
### ✅ Network Operations: [X/4 functions]
### ✅ Volume Operations: [X/5 functions] (+1: volume_prune)
### ✅ Builder Operations: [X/4 functions]
### ✅ System Operations: [X/8 functions] (+1: system_df)
### ✅ Registry Operations: [X/2 functions]
### ✅ Auth Operations: [X/2 functions]

**Total Categories**: 10
**Total Tools**: 56 (up from 51)

## Key Findings
- Array parameter validation: [WORKING/BROKEN]
- Container exec functionality: [WORKING/BROKEN]
- Individual item targeting: [WORKING/BROKEN]

## Cleanup Verification
**Post-test system state**:
- Containers remaining: [count and list]
- Images remaining: [count and list]
- Networks remaining: [count - should be 1 (default)]
- Volumes remaining: [count and list]
- All test resources cleaned: [YES/NO]

## Issues Discovered
[List any failures or regressions]

## Recommendations
[Next steps or concerns]
```

### Save Results
Always save comprehensive test results to:
`/$HOME/code/ACMS/acms_comprehensive_test_results_[D].md`

Where D is the date. Include:
- Complete test results by category
- Success/failure analysis
- Comparison to previous sessions
- Technical evidence of breakthroughs or regressions
- Context for future development sessions

## New Tools Testing Priority (v0.0.9+)

### High Priority - Test These First
1. **container_stats** - Real-time monitoring capability
   - Test with running containers
   - Test `--no-stream` for single snapshot
   - Test both json and table formats

2. **system_df** - Disk usage reporting
   - Verify it shows images, containers, volumes, build cache
   - Compare with actual disk usage

3. **system_version** - Version information
   - Verify version details match expected release

### Medium Priority - Test After Core Functions
4. **volume_prune** - Volume cleanup
   - Create unreferenced volumes, verify cleanup
   - Ensure referenced volumes are NOT pruned

### Updated Tool Testing
- **container run/create**: Test new `--ssh` and `--platform` flags
- **container build**: Test multiple tags with array parameter `["tag1", "tag2"]`

## Usage Instructions for Claude

1. **Read this guide completely** before starting tests
2. **Use TodoWrite tool** to track progress through all 10 categories
3. **Test new tools first** - prioritize the 5 new additions
4. **Test array parameters thoroughly** - this is the most critical functionality
5. **CLEAN UP AFTER EACH CATEGORY** - delete all test resources immediately after testing
6. **Verify cleanup** - run verification commands after completing all tests
7. **Document everything** - save detailed results for future sessions
8. **Compare to previous sessions** - note improvements or regressions
9. **Focus on breakthroughs** - identify what changes between sessions
10. **Emergency cleanup** - if tests are interrupted, run cleanup commands before ending session

## Expected Outcome
ACMS should achieve 100% functionality with all array parameter validation issues resolved. Any regression from this state is significant and should be thoroughly documented.
