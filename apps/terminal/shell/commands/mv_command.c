/*
 * File: mv.c
 *
 * Implements the mv command.
 */

#include "../include/command.h"
#include "../include/host.h"

#include <stdio.h>

static CommandResult mv_execute(
    int argc,
    char **argv
)
{
    CommandResult result;


    result.success = 1;
    result.exit_code = 0;
    result.output = "Move successful.";
    result.error = NULL;


    if (argc < 3)
    {
        result.success = 0;
        result.error = "Usage: mv <source> <destination>";

        return result;
    }


    if (!host_mv(
        argv[1],
        argv[2]
    ))
    {
        result.success = 0;
        result.error = "Failed to move file.";

        return result;
    }


    return result;
}


Command mv_command =
{
    .name = "mv",
    .description = "Move or rename a file",
    .execute = mv_execute
};