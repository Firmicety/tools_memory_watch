if $0=='all' do
    python3 interface/flask/main.py &
    interfacepid=$!
    python3 main/main.py &
    mainFunction=$!
elif $0=='interface' do
    python3 interface/flask/main.py &
    interfacepid=$!
    mainFunction=-1
elif $0=='function' do
    interfacepid=-1
    python3 main/main.py &
    mainFunction=$!
else
    echo 'not a valid parameter'
done