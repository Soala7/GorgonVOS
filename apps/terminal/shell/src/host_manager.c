/*
 * File: VOS/apps/terminal/shell/src/host_manager.c
 *
 * Stores and forwards host callbacks.
 */


#include "../include/host_manager.h"

#include <string.h>


static PWD_CALLBACK pwd_callback = 0;

static LS_CALLBACK ls_callback = 0;

static CD_CALLBACK cd_callback = 0;

static MKDIR_CALLBACK mkdir_callback = 0;

static TOUCH_CALLBACK touch_callback = 0;

static WRITE_CALLBACK write_callback = 0;

static CAT_CALLBACK cat_callback = 0;

static RM_CALLBACK rm_callback = 0;

static RMDIR_CALLBACK rmdir_callback = 0;

static TREE_CALLBACK tree_callback = 0;

static MV_CALLBACK mv_callback = 0;

static CP_CALLBACK cp_callback = 0;

void host_manager_set_pwd(
    PWD_CALLBACK callback
)
{
    pwd_callback = callback;
}


void host_manager_set_ls(
    LS_CALLBACK callback
)
{
    ls_callback = callback;
}


void host_manager_set_cd(
    CD_CALLBACK callback
)
{
    cd_callback = callback;
}


void host_manager_set_mkdir(
    MKDIR_CALLBACK callback
)
{
    mkdir_callback = callback;
}


void host_manager_set_touch(
    TOUCH_CALLBACK callback
)
{
    touch_callback = callback;
}

void host_manager_set_write(
    WRITE_CALLBACK callback
)
{
    write_callback = callback;
}


void host_manager_set_cat(
    CAT_CALLBACK callback
)
{
    cat_callback = callback;
}

void host_manager_set_rm(
    RM_CALLBACK callback
)
{
    rm_callback = callback;
}

void host_manager_set_rmdir(
    RMDIR_CALLBACK callback
)
{
    rmdir_callback = callback;
}

void host_manager_set_tree(
    TREE_CALLBACK callback
)
{
    tree_callback = callback;
}

void host_manager_set_mv(
    MV_CALLBACK callback
)
{
    mv_callback = callback;
}

void host_manager_set_cp(
    CP_CALLBACK callback
)
{
    cp_callback = callback;
}

void host_manager_pwd(
    char *buffer,
    int size
)
{
    if (pwd_callback)
    {
        pwd_callback(
            buffer,
            size
        );

        return;
    }

    strncpy(
        buffer,
        "/",
        size - 1
    );

    buffer[size - 1] = '\0';
}


void host_manager_ls(
    const char *path,
    char *buffer,
    int size
)
{
    if (ls_callback)
    {
        ls_callback(
            path,
            buffer,
            size
        );

        return;
    }



    buffer[0] = '\0';
}


int host_manager_cd(
    const char *path
)
{
    if (cd_callback)
    {
        return cd_callback(path);
    }


    return 0;
}


int host_manager_mkdir(
    const char *path
)
{
    if (mkdir_callback)
    {
        return mkdir_callback(path);
    }


    return 0;
}


int host_manager_touch(
    const char *path
)
{
    if (touch_callback)
    {
        return touch_callback(path);
    }


    return 0;
}


int host_manager_write(
    const char *path,
    const char *content
)
{
    if (write_callback)
    {
        return write_callback(
            path,
            content
        );
    }

    return 0;
}

void host_manager_cat(
    const char *path,
    char *buffer,
    int size
)
{
    if (cat_callback)
    {
        cat_callback(
            path,
            buffer,
            size
        );

        return;
    }


    if (buffer && size > 0)
    {
        buffer[0] = '\0';
    }
}

int host_manager_rm(
    const char *path
)
{
    if (rm_callback)
    {
        return rm_callback(
            path
        );
    }

    return 0;
}

int host_manager_rmdir(
    const char *path
)
{
    if (rmdir_callback)
    {
        return rmdir_callback(path);
    }

    return 0;
}

void host_manager_tree(
    char *buffer,
    int size
)
{
    if (tree_callback)
    {
        tree_callback(
            buffer,
            size
        );

        return;
    }


    if (buffer && size > 0)
    {
        buffer[0] = '\0';
    }
}

int host_manager_mv(
    const char *source,
    const char *destination
)
{
    if (mv_callback)
    {
        return mv_callback(
            source,
            destination
        );
    }

    return 0;
}

int host_manager_cp(
    const char *source,
    const char *destination
)
{
    if (cp_callback)
    {
        return cp_callback(
            source,
            destination
        );
    }

    return 0;
}