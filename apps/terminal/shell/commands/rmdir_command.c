/*
 * File: rmdir.c
 *
 * Implements the rmdir command.
 */

#include "../include/command.h"
#include "../include/host.h"

#include <stdio.h>

static CommandResult rmdir_execute(
    int argc,
    char **argv
)
{
    CommandResult result;


    result.success = 1;
    result.exit_code = 0;
    result.output = "Directory removed.";
    result.error = NULL;


    if (argc < 2)
    {
        result.success = 0;
        result.error = "Usage: rmdir <directory>";

        return result;
    }


    if (!host_rmdir(argv[1]))
    {
        result.success = 0;
        result.error = "Failed to remove directory.";

        return result;
    }


    return result;
}


Command rmdir_command =
{
    .name = "rmdir",
    .description = "Remove an empty directory",
    .execute = rmdir_execute
};