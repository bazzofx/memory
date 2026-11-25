cat > split.py <<'EOF'
f = 'a/b'
proj = f.split('\')[0].split('/')[0]
print(proj)
EOF
python split.py