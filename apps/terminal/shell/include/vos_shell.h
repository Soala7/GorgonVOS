/*
 * File: VOS/apps/terminal/shell/include/vos_shell.h
 *
 * Public API for the VOS shell.
 */

#ifndef VOS_SHELL_H
#define VOS_SHELL_H

#ifdef __cplusplus
extern "C" {
#endif


#include "host_manager.h"



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


void host_register_mv(
    MV_CALLBACK callback
);

void host_register_cp(
    CP_CALLBACK callback
);


void vos_shell_init(void);



const char *vos_shell_execute(
    const char *input
);



void vos_shell_shutdown(void);



#ifdef __cplusplus
}
#endif

#endif