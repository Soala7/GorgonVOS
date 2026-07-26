/*
 * File: write.c
 *
 * Implements the write command.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/command.h"
#include "../include/host.h"


static CommandResult write_execute(
    int argc,
    char **argv
)
{
    CommandResult result;

    result.success = 1;
    result.exit_code = 0;
    result.output = "Write successful.";
    result.error = NULL;


    if (argc < 3)
    {
        result.success = 0;
        result.error = "Usage: write <file> <text>";

        return result;
    }


    /*
     * Build content from argv[2] onwards.
     */
    char *content = malloc(1024);


    if (content == NULL)
    {
        result.success = 0;
        result.error = "Memory allocation failed.";

        return result;
    }


    content[0] = '\0';


    for (int i = 2; i < argc; i++)
    {
        printf("[WRITE COMMAND] file: %s\n", argv[1]);
        printf("[WRITE COMMAND] content: %s\n", content);
        strcat(content, argv[i]);


        if (i < argc - 1)
        {
            strcat(content, " ");
        }
    }



    if (!host_write(
        argv[1],
        content
    ))
    {
        free(content);

        result.success = 0;
        result.error = "Failed to write file.";

        return result;
    }


    free(content);


    return result;
}



Command write_command =
{
    .name = "write",
    .description = "Write text to a file",
    .execute = write_execute
};