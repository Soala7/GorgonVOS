/*
 * File: VOS/apps/terminal/shell/include/host_manager.h
 *
 * Manages callbacks between the C shell and VOS host.
 */

#ifndef HOST_MANAGER_H
#define HOST_MANAGER_H

#ifdef __cplusplus
extern "C" {
#endif

typedef void (*PWD_CALLBACK)(
    char *buffer,
    int size
);

typedef void (*LS_CALLBACK)(
    const char *path,
    char *buffer,
    int size
);

typedef int (*CD_CALLBACK)(
    const char *path
);

typedef int (*MKDIR_CALLBACK)(
    const char *path
);

typedef int (*TOUCH_CALLBACK)(
    const char *path
);

typedef int (*WRITE_CALLBACK)(
    const char *path,
    const char *content
);

typedef void (*CAT_CALLBACK)(
    const char *path,
    char *buffer,
    int size
);

typedef int (*RM_CALLBACK)(
    const char *path
);

typedef int (*RMDIR_CALLBACK)(
    const char *path
);

typedef void (*TREE_CALLBACK)(
    char *buffer,
    int size
);

typedef int (*MV_CALLBACK)(
    const char *source,
    const char *destination
);

typedef int (*CP_CALLBACK)(
    const char *source,
    const char *destination
);

/* ----------------------------
 * Callback registration
 * ---------------------------- */

void host_manager_set_pwd(
    PWD_CALLBACK callback
);

void host_manager_set_ls(
    LS_CALLBACK callback
);

void host_manager_set_cd(
    CD_CALLBACK callback
);

void host_manager_set_mkdir(
    MKDIR_CALLBACK callback
);

void host_manager_set_touch(
    TOUCH_CALLBACK callback
);

void host_manager_set_write(
    WRITE_CALLBACK callback
);

void host_manager_set_cat(
    CAT_CALLBACK callback
);

void host_manager_set_rm(
    RM_CALLBACK callback
);

void host_manager_set_rmdir(
    RMDIR_CALLBACK callback
);

void host_manager_set_tree(
    TREE_CALLBACK callback
);

void host_manager_set_mv(
    MV_CALLBACK callback
);

void host_manager_set_cp(
    CP_CALLBACK callback
);

/* ----------------------------
 * Host operations
 * ---------------------------- */

void host_manager_pwd(
    char *buffer,
    int size
);

void host_manager_ls(
    const char *path,
    char *buffer,
    int size
);

int host_manager_cd(
    const char *path
);

int host_manager_mkdir(
    const char *path
);

int host_manager_touch(
    const char *path
);

int host_manager_write(
    const char *path,
    const char *content
);

void host_manager_cat(
    const char *path,
    char *buffer,
    int size
);

int host_manager_rm(
    const char *path
);

int host_manager_rmdir(
    const char *path
);

void host_manager_tree(
    char *buffer,
    int size
);

int host_manager_mv(
    const char *source,
    const char *destination
);

int host_manager_cp(
    const char *source,
    const char *destination
);

#ifdef __cplusplus
}
#endif

#endif