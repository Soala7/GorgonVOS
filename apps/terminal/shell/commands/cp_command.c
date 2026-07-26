/*
 * File: cp.c
 *
 * Implements the cp command.
 */

#include "../include/command.h"
#include "../include/host.h"

#include <stdio.h>

static CommandResult cp_execute(
    int argc,
    char **argv
)
{
    CommandResult result;


    result.success = 1;
    result.exit_code = 0;
    result.output = "Copy successful.";
    result.error = NULL;


    if (argc < 3)
    {
        result.success = 0;
        result.error = "Usage: cp <source> <destination>";

        return result;
    }


    if (!host_cp(
        argv[1],
        argv[2]
    ))
    {
        result.success = 0;
        result.error = "Failed to copy file.";

        return result;
    }


    return result;
}


Command cp_command =
{
    .name = "cp",
    .description = "Copy a file",
    .execute = cp_execute
};