# Dev Container Troubleshooting

This dev container is for headless KiCad CLI checks and exports. Use native KiCad on Windows for the GUI.

## KiCad version

The container installs KiCad from the official `ppa:kicad/kicad-8.0-releases` PPA and verifies `kicad-cli` reports version `8.x` during the image build. Rebuild the container after changing `.devcontainer/Dockerfile`:

```text
Dev Containers: Rebuild Container
```

After rebuild, confirm:

```bash
kicad-cli version
```

It should print an `8.x` version. The checked-in PCB file requires KiCad 8 or newer.

## Error: Server is null / cannot connect to docker.sock

Example:

```text
"Server":null
failed to connect to the docker API at unix:///var/run/docker.sock
```

This means VS Code found a Docker client, but no Docker daemon is reachable from the environment where the Dev Containers extension is running.

On Windows with Docker Desktop:

1. Start Docker Desktop.
2. Wait until it says the engine is running.
3. In PowerShell, run:

   ```powershell
   docker version
   docker context ls
   ```

4. If using WSL, enable Docker Desktop WSL integration:

   Docker Desktop -> Settings -> Resources -> WSL Integration -> enable your distro.

5. Restart WSL and VS Code:

   ```powershell
   wsl --shutdown
   ```

6. Reopen this folder in VS Code and rebuild the container.

If the folder is opened through WSL, also check inside that WSL distro:

```bash
docker version
ls -l /var/run/docker.sock
```

The Docker client should show a non-null `Server` section before the dev container can build.
