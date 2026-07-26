/*
 * File: VOS/apps/terminal/shell/src/host.c
 *
 * Interface between shell commands and host callbacks.
 */

#include "../include/host.h"
#include "../include/host_manager.h"

#include <stdio.h>

void host_init(void)
{
}

void host_shutdown(void)
{
}

void host_pwd(
    char *buffer,
    int size
)
{
    host_manager_pwd(
        buffer,
        size
    );
}

void host_ls(
    const char *path,
    char *buffer,
    int size
)
{
    if (path == NULL)
    {
        path = "";
    }

    host_manager_ls(
        path,
        buffer,
        size
    );
}

int host_cd(
    const char *path
)
{
    return host_manager_cd(
        path
    );
}

int host_mkdir(
    const char *path
)
{
    return host_manager_mkdir(
        path
    );
}

int host_touch(
    const char *path
)
{
    return host_manager_touch(
        path
    );
}

int host_write(
    const char *path,
    const char *content
)
{
    return host_manager_write(
        path,
        content
    );
}

void host_cat(
    const char *path,
    char *buffer,
    int size
)
{
    printf("[HOST] cat called\n");

    host_manager_cat(
        path,
        buffer,
        size
    );
}

int host_rm(
    const char *path
)
{
    printf("[HOST] rm called\n");

    return host_manager_rm(
        path
    );
}

int host_rmdir(
    const char *path
)
{
    printf("[HOST] rmdir called\n");

    return host_manager_rmdir(
        path
    );
}

void host_tree(
    char *buffer,
    int size
)
{
    printf("[HOST] tree called\n");

    host_manager_tree(
        buffer,
        size
    );
}

int host_mv(
    const char *source,
    const char *destination
)
{
    printf("[HOST] mv called\n");

    return host_manager_mv(
        source,
        destination
    );
}

int host_cp(
    const char *source,
    const char *destination
)
{
    printf("[HOST] cp called\n");

    return host_manager_cp(
        source,
        destination
    );
}