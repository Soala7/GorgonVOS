/*
 * File: VOS/apps/terminal/shell/include/host.h
 *
 * Host interface between the shell and VOS.
 */

#ifndef HOST_H
#define HOST_H

#ifdef __cplusplus
extern "C" {
#endif

#include "host_manager.h"

/*
 * Initialization
 */

void host_init(void);
void host_shutdown(void);


/*
 * Filesystem operations
 */

void host_pwd(
    char *buffer,
    int size
);

void host_ls(
    const char *path,
    char *buffer,
    int size
);

int host_cd(
    const char *path
);

int host_mkdir(
    const char *path
);

int host_touch(
    const char *path
);

int host_write(
    const char *path,
    const char *content
);

void host_cat(
    const char *path,
    char *buffer,
    int size
);

int host_rm(
    const char *path
);

int host_rmdir(
    const char *path
);

void host_tree(
    char *buffer,
    int size
);

int host_mv(
    const char *source,
    const char *destination
);

int host_cp(
    const char *source,
    const char *destination
);

/*
 * Callback registration
 */

void host_register_pwd(
    PWD_CALLBACK callback
);

void host_register_ls(
    LS_CALLBACK callback
);

void host_register_cd(
    CD_CALLBACK callback
);

void host_register_mkdir(
    MKDIR_CALLBACK callback
);

void host_register_touch(
    TOUCH_CALLBACK callback
);

void host_register_write(
    WRITE_CALLBACK callback
);

void host_register_cat(
    CAT_CALLBACK callback
);

void host_register_rm(
    RM_CALLBACK callback
);

void host_register_rmdir(
    RMDIR_CALLBACK callback
);

void host_register_tree(
    TREE_CALLBACK callback
);

void host_register_mv(
    MV_CALLBACK callback
);

void host_register_cp(
    CP_CALLBACK callback
);

#ifdef __cplusplus
}
#endif

#endif