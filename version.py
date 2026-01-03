"""
Script de gerenciamento de versão do projeto.
Atualiza VERSION, CHANGELOG.md e cria git tags.
"""
import sys
import re
from datetime import datetime
from pathlib import Path


def get_current_version():
    """Lê a versão atual do arquivo VERSION."""
    version_file = Path("VERSION")
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"


def bump_version(current_version, bump_type="patch"):
    """
    Incrementa a versão seguindo SemVer.
    
    Args:
        current_version: Versão atual (ex: "1.0.0")
        bump_type: Tipo de incremento ("major", "minor", "patch")
        
    Returns:
        Nova versão
    """
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    
    return f"{major}.{minor}.{patch}"


def update_version_file(new_version):
    """Atualiza o arquivo VERSION."""
    Path("VERSION").write_text(new_version)
    print(f"✓ VERSION atualizado para {new_version}")


def update_changelog(new_version, changes):
    """Adiciona nova entrada no CHANGELOG.md."""
    changelog_path = Path("CHANGELOG.md")
    
    if not changelog_path.exists():
        print("❌ CHANGELOG.md não encontrado!")
        return
    
    content = changelog_path.read_text(encoding='utf-8')
    
    # Encontra posição para inserir nova versão
    today = datetime.now().strftime("%Y-%m-%d")
    
    new_entry = f"""
## [{new_version}] - {today}

{changes}

"""
    
    # Insere após o cabeçalho
    lines = content.split('\n')
    insert_pos = None
    for i, line in enumerate(lines):
        if line.startswith('## [') and ']' in line:
            insert_pos = i
            break
    
    if insert_pos:
        lines.insert(insert_pos, new_entry)
        changelog_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"✓ CHANGELOG.md atualizado com versão {new_version}")
    else:
        print("⚠️  Não foi possível atualizar CHANGELOG.md automaticamente")


def show_usage():
    """Mostra instruções de uso."""
    print("""
🏷️  Script de Versionamento

Uso:
    python version.py <tipo> [mensagem]

Tipos:
    major  - Incrementa versão principal (1.0.0 → 2.0.0)
    minor  - Incrementa versão secundária (1.0.0 → 1.1.0)
    patch  - Incrementa patch (1.0.0 → 1.0.1)
    show   - Mostra versão atual

Exemplo:
    python version.py minor "Adiciona nova funcionalidade X"
    python version.py patch "Corrige bug Y"
    python version.py show
""")


def main():
    if len(sys.argv) < 2:
        show_usage()
        return
    
    command = sys.argv[1].lower()
    
    current = get_current_version()
    
    if command == "show":
        print(f"📌 Versão atual: {current}")
        return
    
    if command not in ["major", "minor", "patch"]:
        print(f"❌ Tipo inválido: {command}")
        show_usage()
        return
    
    # Nova versão
    new_version = bump_version(current, command)
    
    print(f"\n🎯 Atualizando versão: {current} → {new_version}")
    
    # Mensagem de mudança
    change_msg = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else f"{command.capitalize()} update"
    
    # Atualiza arquivos
    update_version_file(new_version)
    
    # Instrução para CHANGELOG
    print(f"\n📝 Próximo passo:")
    print(f"   1. Edite CHANGELOG.md e adicione as mudanças da versão {new_version}")
    print(f"   2. Execute:")
    print(f"      git add VERSION CHANGELOG.md README.md")
    print(f"      git commit -m 'chore: bump version to {new_version}'")
    print(f"      git tag -a v{new_version} -m 'Release {new_version}'")
    print(f"      git push && git push --tags")


if __name__ == "__main__":
    main()
