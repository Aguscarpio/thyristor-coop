# pid=$(ps -A|grep "python3"|rev|cut -d ' ' -f 1|rev); \
pid=1; \
while [ "$pid" != "" ]; do ps -A|grep -wE "54122|54106|54124|54118|54108|54100|54098|54116|54112|54120|54110|54104|54114|54102" > /dev/null; \
if [ $? -eq 0 ]; then sleep 20;else pid=""; fi; done; \
python3 run.py -ncpus 4 -dimRs 840 -dimIin 840 -N_steps 1250000 -dt 0.002 -Cm 10.0 -direction up &
python3 run.py -ncpus 4 -dimRs 840 -dimIin 840 -N_steps 1250000 -dt 0.002 -Cm 10.0 -direction right &
python3 run.py -ncpus 4 -dimRs 840 -dimIin 840 -N_steps 1250000 -dt 0.002 -Cm 10.0 -direction left &
python3 run.py -ncpus 4 -dimRs 840 -dimIin 840 -N_steps 1250000 -dt 0.002 -Cm 10.0 -direction down &
