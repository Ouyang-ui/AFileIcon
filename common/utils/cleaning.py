import glob
import os
import shutil
import sublime
import sublime_plugin

from . import path
from .. import settings

from .logging import log, dump, message


def _get_patches(dir, pattern):
    for dirname, subdirs, files in os.walk(dir):
        for f in files:
            if f.endswith(pattern):
                yield os.path.join(dirname, f)


def clean_all():
    message("Cleaning up")
    overlay_path = path.get_overlay()

    if os.path.exists(overlay_path):
        try:
            shutil.rmtree(overlay_path)
        except Exception as error:
            log("Error during cleaning")
            dump(error)
        else:
            message("Cleaned up successfully")


def clean_patches():
    log("Cleaning patches")
    overlay_path = path.get_overlay()
    patches = _get_patches(overlay_path, ".sublime-theme")

    if os.path.exists(overlay_path):
        try:
            for p in patches:
                os.remove(p)
        except Exception as error:
            log("Error during cleaning")
            dump(error)
        else:
            log("Cleaned up successfully")
            sublime.run_command("afi_patch_themes")


def revert():
    log("Reverting to a freshly installed state")

    try:
        shutil.rmtree(path.get_overlay_cache(), ignore_errors=True)
        shutil.rmtree(path.get_overlay(), ignore_errors=True)
    except Exception as error:
        log("Error during reverting")
        dump(error)
    else:
        log("Reverted successfully")
        sublime.run_command("afi_reload")


class AfiCleanCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.set_timeout_async(clean_patches)


class AfiRevertCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.set_timeout_async(revert)
