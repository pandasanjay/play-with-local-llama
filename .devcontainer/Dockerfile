# Multi-stage build: use a builder stage for compilation and a smaller final image
# Builder stage with full development environment
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04 AS builder

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    git \
    wget \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up locales
RUN locale-gen en_US.UTF-8

# Make Python 3.10 the default
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Install uv - Fast Python package manager and resolver
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH - this line is critical!
ENV PATH="/root/.local/bin:$PATH"

# Make sure uv is also in the default user's PATH
RUN mkdir -p /usr/local/bin && ln -s /root/.local/bin/uv /usr/local/bin/uv

# ========== DEPENDENCY CACHING STRATEGY ==========
# Copy just requirements for dependency installation
WORKDIR /tmp
COPY requirements.txt pyproject.toml ./

# Install dependencies with caching strategy
# 1. Core dependencies
RUN uv pip install --system --upgrade pip

# 2. Create a virtual environment using uv instead of python -m venv
# We still need python3.10-venv package as uv uses Python's venv module under the hood
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 3. PyTorch (largest dependency) in its own layer
# Using the virtual environment ensures binaries are compiled once
RUN uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. Core requirements
RUN uv pip install -r requirements.txt

# 5. ML Libraries
RUN uv pip install transformers accelerate bitsandbytes

# 6. Development tools in their own layer
RUN uv pip install black flake8 mypy ruff ipython jupyterlab

# ========== FINAL STAGE ==========
# Use runtime image for final stage - smaller than development image
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PATH="/opt/venv/bin:$PATH" \
    CUDA_HOME="/usr/local/cuda" \
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    locales \
    git \
    zsh \
    zsh-autosuggestions \
    zsh-syntax-highlighting \
    fonts-powerline \
    sudo \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Install Node.js v20.x and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && \
    ln -sf /usr/bin/python3.10 /usr/bin/python3

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Verify installations
RUN python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Create a non-root user 'vscode' with sudo access
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Fix permissions for VS Code Server
# First remove .vscode-server if it exists with wrong permissions
RUN rm -rf /home/$USERNAME/.vscode-server

# Create VS Code Server directories with proper permissions
RUN mkdir -p /home/$USERNAME/.vscode-server \
    && mkdir -p /home/$USERNAME/.vscode-server/extensions \
    && mkdir -p /home/$USERNAME/.vscode-server/data/Machine \
    && mkdir -p /home/$USERNAME/.vscode-server/data/User \
    && mkdir -p /home/$USERNAME/.vscode-server/bin \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME \
    && chmod -R 755 /home/$USERNAME

# Install uv for the runtime environment (as root)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv's default install location to PATH for subsequent root commands
ENV PATH="/root/.local/bin:${PATH}"

# Make uv available system-wide with correct permissions
RUN mkdir -p /usr/local/bin && \
    ln -sf /root/.local/bin/uv /usr/local/bin/uv && \
    chmod 755 /root/.local/bin/uv && \
    chmod 755 /usr/local/bin/uv

# Switch to vscode user for Oh My Zsh installation
USER $USERNAME
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Configure zsh with Oh My Zsh
RUN echo 'export HISTFILE=~/.zsh_history' >> /home/$USERNAME/.zshrc \
    && echo 'export HISTSIZE=10000' >> /home/$USERNAME/.zshrc \
    && echo 'export SAVEHIST=10000' >> /home/$USERNAME/.zshrc \
    && echo 'setopt APPEND_HISTORY' >> /home/$USERNAME/.zshrc \
    && echo 'setopt SHARE_HISTORY' >> /home/$USERNAME/.zshrc \
    && echo 'setopt HIST_IGNORE_DUPS' >> /home/$USERNAME/.zshrc \
    && echo 'setopt HIST_FIND_NO_DUPS' >> /home/$USERNAME/.zshrc \
    && echo 'setopt HIST_REDUCE_BLANKS' >> /home/$USERNAME/.zshrc \
    && echo 'setopt HIST_VERIFY' >> /home/$USERNAME/.zshrc \
    && echo 'source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh' >> /home/$USERNAME/.zshrc \
    && echo 'source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> /home/$USERNAME/.zshrc \
    && echo 'alias ll="ls -la"' >> /home/$USERNAME/.zshrc \
    && echo 'alias python=python3' >> /home/$USERNAME/.zshrc \
    && echo 'alias pip=pip3' >> /home/$USERNAME/.zshrc \
    && echo 'export PATH="/opt/venv/bin:$PATH"' >> /home/$USERNAME/.zshrc \
    && sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="clean"/' /home/$USERNAME/.zshrc \
    && sed -i 's/plugins=(git)/plugins=(git pip python docker)/' /home/$USERNAME/.zshrc

# Switch back to root for remaining setup
USER root

# Set working directory to workspace
WORKDIR /workspace

# Use zsh as default shell
CMD ["zsh"]