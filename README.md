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
   pip install boto3
   ```
3. **Run the interactive installer**
   ```bash
   python scripts/interactive_installer.py
   ```
4. **Start CloudLens**
   ```bash
   python cloudlens.py
   ```
