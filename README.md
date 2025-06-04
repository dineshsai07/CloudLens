# CloudLens
An intelligent, open-source platform that proactively optimizes cloud costs, reduces resource waste, and promotes sustainable cloud practices—built by the DevOps community, for the DevOps community.

## 🖥️ Prerequisites
- Docker & Docker Compose
- `kubectl` CLI (if using k3d/kind)
- Python 3.8+
- Terraform 1.5+

## 🚀 Quickstart (Local-Only)
1. **Clone & enter project**
   ```bash
   git clone https://github.com/<your-org>/CloudLens.git
   cd CloudLens
   ```
2. **Install Python dependencies**
   ```bash
   pip install boto3 flask azure-identity google-auth
   ```
3. **Run the interactive installer (web UI)**
   ```bash
   python cloudlens_web.py
   ```
   Then open `http://localhost:5000` in your browser and follow the prompts.
   The web UI features a sleek gradient theme and displays cost charts that update as you check potential savings.
4. **Run the CLI tool** (optional)
   ```bash
   python scripts/interactive_installer.py
   ```
5. **Start CloudLens from the command line**
   ```bash
   python cloudlens.py
   ```
