/*
 * File: VOS/apps/terminal/shell/commands/about_command.c
 */

#include "../include/command.h"
#include "../include/command_result_builder.h"
#include "../include/version.h"

#include <stdio.h>


static CommandResult about_execute(int argc, char **argv)
{
    (void)argc;
    (void)argv;

    char *output = result_alloc(2048);

    if (output == NULL)
    {
        return result_error("Memory allocation failed.");
    }

    snprintf(
        output,
        2048,

        "Gorgon OS (VOS)\n"
        "\n"

        "Version : %s\n"
        "Build   : %s\n"
        "Phase   : 1 - Virtual OS\n"
        "\n"

        "Developer : Soala7\n"
        "\n"

        "About VOS\n"
        "  Gorgon OS (VOS) is a virtual operating system project\n"
        "  built to explore how operating systems work from the\n"
        "  inside out.\n"
        "\n"

        "Phase 1\n"
        "  VOS currently provides a simulated operating environment\n"
        "  containing its own filesystem, storage, processes,\n"
        "  applications, users, terminal, and desktop environment.\n"
        "\n"

        "Technology\n"
        "  - Python\n"
        "  - C\n"
        "\n"

        "Development Roadmap\n"
        "  Phase 1 - Virtual OS\n"
        "  Phase 2 - Semi-real OS\n"
        "  Phase 3 - Real OS\n"
        "\n"

        "Goal\n"
        "  Evolve VOS from a virtual operating environment into\n"
        "  a real operating system capable of interacting directly\n"
        "  with computer hardware.\n"
        "\n"

        "Built by Soala7\n",

        vos_version(),
        vos_build()
    );

    return result_success(output);
}


Command about_command =
{
    .name = "about",
    .description = "Display information about Gorgon OS",
    .execute = about_execute
};