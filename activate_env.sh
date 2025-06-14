#!/bin/bash
# Script para ativar o ambiente virtual do projeto Mozart APS2

echo "🎵 Ativando ambiente Python para Mozart APS2..."
source .venv/bin/activate

echo "✅ Ambiente ativado!"
echo "📍 Python: $(python --version)"
echo "📍 Local: $(which python)"
echo ""
echo "💡 Comandos disponíveis:"
echo "   pytest                    # Executar testes"
echo "   black src/ tests/         # Formatar código"
echo "   flake8 src/ tests/        # Verificar qualidade"
echo "   python scripts/train_model.py  # Treinar modelo"
echo ""