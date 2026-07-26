/*
 * File: VOS/apps/terminal/shell/src/vos_shell.c
 *
 * Public API for the VOS shell.
 */


#include "../include/vos_shell.h"

#include "../include/shell.h"
#include "../include/command_loader.h"
#include "../include/command_registry.h"
#include "../include/command_result.h"
#include "../include/host_manager.h"
#include "../include/host.h"

#include <string.h>




void vos_shell_init(void)
{
    registry_init();

    host_init();

    load_commands();
}




void host_register_pwd(
    PWD_CALLBACK callback
)
{
    host_manager_set_pwd(
        callback
    );
}




void host_register_ls(
    LS_CALLBACK callback
)
{
    host_manager_set_ls(
        callback
    );
}




void host_register_cd(
    CD_CALLBACK callback
)
{
    host_manager_set_cd(
        callback
    );
}




void host_register_mkdir(
    MKDIR_CALLBACK callback
)
{
    host_manager_set_mkdir(
        callback
    );
}




void host_register_touch(
    TOUCH_CALLBACK callback
)
{
    host_manager_set_touch(
        callback
    );
}


void host_register_write(
    WRITE_CALLBACK callback
)
{
    host_manager_set_write(
        callback
    );
}

void host_register_cat(
    CAT_CALLBACK callback
)
{
    host_manager_set_cat(
        callback
    );
}

void host_register_rm(
    RM_CALLBACK callback
)
{
    host_manager_set_rm(
        callback
    );
}

void host_register_rmdir(
    RMDIR_CALLBACK callback
)
{
    host_manager_set_rmdir(
        callback
    );
}

void host_register_tree(
    TREE_CALLBACK callback
)
{
    host_manager_set_tree(
        callback
    );
}

void host_register_mv(
    MV_CALLBACK callback
)
{
    host_manager_set_mv(
        callback
    );
}

void host_register_cp(
    CP_CALLBACK callback
)
{
    host_manager_set_cp(
        callback
    );
}

const char *vos_shell_execute(
    const char *input
)
{
    static char output[4096];


    CommandResult result;


    result = shell_execute(
        (char *)input
    );



    if (result.success)
    {
        if (result.output != NULL)
        {
            strncpy(
                output,
                result.output,
                sizeof(output) - 1
            );

            output[sizeof(output) - 1] = '\0';
        }
        else
        {
            output[0] = '\0';
        }
    }
    else
    {
        if (result.error != NULL)
        {
            strncpy(
                output,
                result.error,
                sizeof(output) - 1
            );

            output[sizeof(output) - 1] = '\0';
        }
        else
        {
            strcpy(
                output,
                "Unknown shell error."
            );
        }
    }


    return output;
}





void vos_shell_shutdown(void)
{
    host_shutdown();
}