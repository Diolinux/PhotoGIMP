# Criar o script
cat > ~/instalar_photogimp.sh << 'EOF'
#!/bin/bash
# Script para instalar PhotoGIMP no GIMP 3.2 (Zorin OS)

echo "=========================================="
echo "  PhotoGIMP Installer para GIMP 3.2"
echo "=========================================="
echo ""

ZIP_FILE="$HOME/Transferências/PhotoGIMP-master.zip"

if [ ! -f "$ZIP_FILE" ]; then
    echo "❌ ERRO: Ficheiro PhotoGIMP-master.zip não encontrado!"
    echo "   Local esperado: $ZIP_FILE"
    echo ""
    echo "Por favor, descarregue o ficheiro de:"
    echo "https://github.com/Diolinux/PhotoGIMP"
    echo ""
    exit 1
fi

echo "✅ Ficheiro ZIP encontrado: $ZIP_FILE"
echo ""

if ! command -v gimp &> /dev/null; then
    echo "❌ ERRO: GIMP não está instalado!"
    echo "   Instale com: sudo apt install gimp"
    echo ""
    exit 1
fi

echo "✅ GIMP instalado: $(gimp --version | head -1)"
echo ""

echo "🔒 Fechando o GIMP (se estiver aberto)..."
pkill -f gimp 2>/dev/null
sleep 2

echo "📦 Extraindo ficheiros..."
cd /tmp
rm -rf /tmp/photogimp
unzip -q "$ZIP_FILE" -d /tmp/photogimp/

if [ $? -ne 0 ]; then
    echo "❌ ERRO: Falha ao extrair o ficheiro ZIP!"
    exit 1
fi
echo "✅ Extração concluída!"
echo ""

echo "📂 Copiando configurações do PhotoGIMP..."
mkdir -p ~/.config/GIMP/3.2/
cp -rf /tmp/photogimp/PhotoGIMP-master/.config/GIMP/3.0/* ~/.config/GIMP/3.2/

if [ $? -ne 0 ]; then
    echo "❌ ERRO: Falha ao copiar configurações!"
    exit 1
fi
echo "✅ Configurações copiadas!"

echo "🖼️  Copiando ícones..."
cp -rf /tmp/photogimp/PhotoGIMP-master/.local/share/* ~/.local/share/
echo "✅ Ícones copiados!"

echo "🔄 Atualizando menu de aplicações..."
update-desktop-database ~/.local/share/applications/ 2>/dev/null
echo "✅ Menu atualizado!"

echo "🧹 Limpando cache do GIMP..."
rm -rf ~/.cache/gimp*
echo "✅ Cache limpa!"

rm -rf /tmp/photogimp

echo ""
echo "=========================================="
echo "✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=========================================="
echo ""
echo "📌 Para abrir o GIMP:"
echo "   gimp"
echo "   ou procure no menu de aplicações"
echo ""
echo "📌 Teste o atalho Ctrl+J para duplicar camadas"
echo "=========================================="
EOF

# Dar permissão
chmod +x ~/instalar_photogimp.sh

echo "✅ Script criado em: ~/instalar_photogimp.sh"
echo "   Para usar: ~/instalar_photogimp.sh"