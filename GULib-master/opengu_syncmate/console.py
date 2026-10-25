"""Desktop console uses the same installed, committed OpenGU submission path."""
from argparse import Namespace

from syncmate_core import context, versions
from syncmate_core.controller import Controller, readiness
from .adapter import OpenGUProjectExtension


class ConsoleExtension(OpenGUProjectExtension):
    def __init__(self, *, source_ref, verification_root=None):
        super().__init__(verification_root=verification_root)
        self.source_ref = source_ref

    def recipe_ids(self, project_root):
        from pathlib import Path
        source = versions.GitSource(project_root, self.source_ref)
        return tuple(Path(path).stem for path in source.files('scripts/syncmate/recipes') if path.endswith('.yaml'))


class OpenGUConsole(Controller):
    def __init__(self, project, *, source_ref, verification_root=None):
        super().__init__(project, source_ref=source_ref)
        self.verification_root = verification_root

    def readiness(self, node_id, recipe):
        from .control import preview
        try:
            source = versions.GitSource(self.project.root, self.source_ref)
            # The private consumer verifies its package/deployment policy first.
            with self.bind(node_id):
                private = preview(self.project.root, recipe, node_id, self.project.device_file,
                                  source.sha, self.verification_root)
                checked = readiness(node_id, recipe, source.sha)
            checked['preview'] = private
            return checked
        except (Exception, SystemExit) as exc:
            return {'ready': False, 'errors': [str(exc)]}

    def dispatch_job(self, saved, device, warnings):
        from .control import dispatch
        args = Namespace(job_id=saved['job_id'], recipe=saved['recipe'], node_id=saved['node_id'],
                         config=self.project.device_file, wait=False)
        with self.bind(saved['node_id']):
            return dispatch(args, source_ref=saved['binding']['git_sha'],
                            verification_root=self.verification_root)


def serve(root, args, *, source_ref, verification_root=None):
    from syncmate_core import console
    extension = ConsoleExtension(source_ref=source_ref, verification_root=verification_root)
    with context.use(root, extension=extension) as project:
        if args.stop:
            return console.cmd_console(args)
        # Scientific imports occur in AAGU-103's fresh committed-source worker.
        # Never import mutable experiments into this long-lived HTTP process.
        console.serve_console({root.name: project}, args.port, args.desktop,
            controller_factory=lambda p: OpenGUConsole(p, source_ref=source_ref,
                                                       verification_root=verification_root))
    return 0
