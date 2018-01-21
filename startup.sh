cd /home/pi/projects/dorm-lights/
for i in {1..90}; do ping -c1 www.google.com &> /dev/null && break; done
python lights_app.py
