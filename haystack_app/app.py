from service import create_app
import time

t = 60

print("waiting elastic server on...")
for i in range(t):
    time.sleep(1)
    print(f"loadging time...{i+1}/{t}")
print("waiting elastic server on done")

print("start flask app...")
create_app().run(port=7777, debug=False)
