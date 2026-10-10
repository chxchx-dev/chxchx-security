import os
import subprocess
import tarfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[1]
REMOTE_INSTALLER = PROJECT_ROOT / "install-remote-fedora.sh"


def test_remote_installer_extracts_source_and_forwards_arguments(tmp_path):
    source_root = tmp_path / "source" / "repo"
    source_root.mkdir(parents=True)
    installer = source_root / "install-fedora.sh"
    installer.write_text(
        '#!/usr/bin/env bash\nprintf \'<%s>\\n\' "$@"\n',
        encoding="utf-8",
    )
    installer.chmod(0o755)

    archive = tmp_path / "source.tar.gz"
    with tarfile.open(archive, "w:gz") as bundle:
        bundle.add(installer, arcname="repository/install-fedora.sh")

    install_dir = tmp_path / "local-install"
    environment = os.environ.copy()
    environment["CHXSEC_SOURCE_ARCHIVE_URL"] = archive.as_uri()
    environment["CHXSEC_INSTALL_DIR"] = str(install_dir)

    result = subprocess.run(
        ["bash", str(REMOTE_INSTALLER), "--dry-run", "--with-dev"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
        timeout=15,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[-2:] == ["<--dry-run>", "<--with-dev>"]
    assert (install_dir / "install-fedora.sh").is_file()
