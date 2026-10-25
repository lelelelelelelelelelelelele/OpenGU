"""The console prepares native project libraries before starting HTTP threads."""
import importlib.util
from pathlib import Path
import threading


def load_entry():
    path = Path(__file__).resolve().parents[1] / 'scripts/syncmate/syncmate.py'
    spec = importlib.util.spec_from_file_location('_console_startup_entry', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_console_prepares_on_main_thread_before_serving(monkeypatch):
    entry = load_entry()
    calls = []
    monkeypatch.setattr(entry, 'deployment_policy', lambda root: {'require_origin_main': False})
    monkeypatch.setattr(entry, 'prepare_console_runtime', lambda: calls.append(('prepare', threading.get_ident())))
    from syncmate_core import console
    monkeypatch.setattr(console, 'serve_console', lambda *a: calls.append(('serve', threading.get_ident())))
    assert entry.main(['console', '--port', '0']) == 0
    assert calls == [('prepare', threading.main_thread().ident), ('serve', threading.main_thread().ident)]


def test_other_cli_commands_do_not_prepare_numerical_runtime(monkeypatch):
    entry = load_entry()
    monkeypatch.setattr(entry, 'deployment_policy', lambda root: {'require_origin_main': False})
    def unexpected():
        raise AssertionError('Non-console CLI must remain lightweight')
    monkeypatch.setattr(entry, 'prepare_console_runtime', unexpected)
    monkeypatch.setattr(entry, 'core_main', lambda *a, **kw: 17)
    assert entry.main(['smoke', '--json']) == 17


def test_console_stop_does_not_load_numerical_runtime(monkeypatch):
    entry = load_entry()
    monkeypatch.setattr(entry, 'deployment_policy', lambda root: {'require_origin_main': False})
    def unexpected():
        raise AssertionError('Stopping the local observer must remain lightweight')
    monkeypatch.setattr(entry, 'prepare_console_runtime', unexpected)
    from syncmate_core import console
    monkeypatch.setattr(console, 'cmd_console', lambda args: 23)
    assert entry.main(['console', '--stop']) == 23
