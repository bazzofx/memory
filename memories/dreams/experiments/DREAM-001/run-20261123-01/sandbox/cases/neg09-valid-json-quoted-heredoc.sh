cat > ok.json <<'EOF'
{"path": "C:\\ai\\memories", "nl": "a\nb", "u": "\u00e9"}
EOF
python -m json.tool ok.json