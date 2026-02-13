# Menu Update - Quick Reference Guide

## 🚀 Começar Rápido

### Para Usuários
```bash
python3 main.py
# Menu abre automaticamente com botões estilizados
```

### Controles do Menu
- **↑ / ↓** - Mudar seleção
- **ENTER** - Confirmar
- **ESC** - Sair do menu principal
- **Mouse** - Hover e clique em botões

---

## 🎮 Menu Screen

```
╔═══════════════════════════════════╗
║                                   ║
║  PYTHON 2D GAME DEMO              ║  (Título em branco)
║                                   ║
║     ┌──────────────────────┐      ║
║     │ ► JOGAR ◀            │      ║  (Botão selecionado em neon)
║     └──────────────────────┘      ║
║                                   ║
║     ┌──────────────────────┐      ║
║     │   CONTROLES          │      ║  (Botão normal)
║     └──────────────────────┘      ║
║                                   ║
║     ┌──────────────────────┐      ║
║     │   SAIR               │      ║  (Botão normal)
║     └──────────────────────┘      ║
║                                   ║
╚═══════════════════════════════════╝
```

### Botões Estilizados
- **Normal:** Azul escuro (#1A2D5A) com borda ciano opaco (#00B4DC)
- **Hover/Selected:** Azul claro (#144B96) com borda neon (#00FFFF)
- **Overlay:** Camada escura 100% alpha para legibilidade

---

## 🔧 Mudanças no Código

### Arquivo Modificado
- [main.py](main.py)

### Funções Adicionadas
1. `load_menu_bg()` - Carrega background (linha ~414)
2. `class Button` - Classe de botão estilizado (linha ~442)
3. `draw_menu()` - Renderiza menu completo (linha ~510)
4. `handle_menu_input()` - Processa input (linha ~543)
5. `draw_button()` - Helper para desenhar botão (linha ~478)

### Seções Alteradas
- **Inicialização:** Botões e menu_bg carregados (linha ~831)
- **Eventos:** Nova lógica de input do menu (linha ~863)
- **Draw:** Simplificado para uma chamada (linha ~1049)

---

## 📁 Arquivo de Background Futuro

**Local:** `assets/images/ui/menu_bg.png`

### Como Trocar APENAS a Imagem (sem código)
```bash
# Localizar o arquivo atual
ls -la assets/images/ui/menu_bg.png

# Fazer backup
cp assets/images/ui/menu_bg.png assets/images/ui/menu_bg.png.bak

# Substituir por nova imagem
cp /seu/novo/menu_bg.png assets/images/ui/menu_bg.png

# Pronto! O jogo carrega automaticamente
```

### Especificações Recomendadas
- **Resolução:** 960×540px (exato)
- **Formato:** PNG, JPG ou BMP
- **Estilo:** Cyber/Neon para coerência
- **Cores:** Azuis, cians e roxos

---

## 🎯 Fluxo de Uso

### Primeira Execução
```
1. App inicia
2. Menu aparece com "PYTHON 2D GAME DEMO"
3. 3 botões: JOGAR | CONTROLES | SAIR
4. Selecione com setas ↑/↓ ou mouse
5. Pressione ENTER ou clique
```

### Durante Jogo
```
1. Jogue normalmente
2. Pressione ESC para voltar ao menu
3. Menu reaparece, score resetado
4. Escolha JOGAR para reiniciar
```

### Painel de Controles
```
1. No menu, selecione "CONTROLES"
2. Painel mostra:
   - A/D ou <-/-> : Mover
   - SPACE/W/^ : Pular
   - F : Atirar
   - ESC : Menu
3. Pressione ESC para voltar
```

---

## 🛠️ Para Desenvolvedores

### Adicionar Novo Botão
```python
# Em main():
buttons.append(Button("NOVO", WIDTH // 2 - 100, 430, 200, 50))

# Em handle_menu_input():
actions = ['play', 'controls', 'quit', 'novo_action']
```

### Customizar Cores
Edite em `main.py` (linhas ~463-471):
```python
fill_color = (25, 45, 90)      # Azul escuro
border_color = (0, 180, 220)   # Ciano opaco
text_color = (200, 200, 200)   # Cinza texto
```

### Mudar Posição de Botões
Edite em `main()`:
```python
buttons = [
    Button("JOGAR", x, y, width, height),
    Button("...", ...),
]
```

---

## ✅ Validação

### Testes Passando
- ✓ Menu background carregado
- ✓ Botões criados
- ✓ Menu renderizado
- ✓ Input teclado funcional
- ✓ Input mouse funcional
- ✓ Painel de controles funcional

### Estados Preservados
- ✓ PLAYING (gameplay normal)
- ✓ GAME_OVER (tela de game over)
- ✓ LEVEL_COMPLETE (tela de conclusão)
- ✓ Score e estatísticas intactas

---

## 📝 Checklist de Uso

- [ ] Executar `python3 main.py`
- [ ] Verificar se menu aparece
- [ ] Testar navegação com setas
- [ ] Testar clique em botões
- [ ] Testar "JOGAR" para iniciar jogo
- [ ] Testar "CONTROLES" para painel
- [ ] ESC para voltar ao menu
- [ ] ESC durante jogo volta ao menu
- [ ] "SAIR" encerra aplicação
- [ ] Trocar `menu_bg.png` sem alterar código

---

## 🎨 Anatomia do Botão

```
┌─ Button(label, x, y, width, height) ─┐
│                                       │
│  [JOGAR]  ← label                    │
│  (x, y)   ← posição no menu          │
│  200×50   ← dimensões                │
│                                       │
│  Cores ao hover:                      │
│  - Fundo: azul claro                 │
│  - Borda: ciano neon                 │
│  - Texto: branco brilhante           │
│                                       │
└───────────────────────────────────────┘
```

---

## 🔗 Arquivos Relacionados

- [main.py](main.py) - Principal
- [MENU_UPDATE.md](MENU_UPDATE.md) - Documentação completa
- [MODIFICATIONS.md](MODIFICATIONS.md) - Detalhes técnicos
- [assets/images/ui/menu_bg.png](assets/images/ui/menu_bg.png) - Background do menu
- [requirements.txt](requirements.txt) - Dependências

---

## ❓ Perguntas Frequentes

**P: Como mudo apenas o background?**
A: Substitua `assets/images/ui/menu_bg.png` - nenhuma alteração de código necessária.

**P: Como adiciono mais controles?**
A: Veja seção "Para Desenvolvedores" acima.

**P: Se o background não existir?**
A: Fallback automático para surface azul escuro.

**P: Menu funciona com mouse e teclado?**
A: Sim, ambos simultâneos - hover com mouse, navegação com setas e ENTER.

---

Generated: feb 2026
Version: 1.0
Status: ✓ Production Ready

