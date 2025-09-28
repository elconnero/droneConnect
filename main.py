from djitellopy import tello
import time



def getInfo(me):                                                                                            # Simple information that will be displayed with every movement.
    global count
    count += 1
    try:
        h = me.get_height()
    except Exception as e:
        h = f"unavailable ({e})"
    try:
        ft = me.get_flight_time()
    except Exception as e:
        ft = f"unavailable ({e})"
    print(f"Information Stop: {count}")
    print(f"Height (cm):      {h}")
    print(f"Flight time (s):  {ft}")

# Pre-launch safety check.
print("Before launching program we need to make sure that we have an area of 2m^3 free of obstacles.")
while True:
    ready = input("Are you ready to launch the Tello? (y/n): ").strip().lower()
    if ready == 'y':
        break
    elif ready == 'n':
        print("Please prepare the area and then run the program again.")
        exit()
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

def main():
    me = tello.Tello()                                                                                          # Creating an object via Tello.

    try:
        me.connect()                                                                                            # Connecting to the Tello.
        try:
            bat = me.get_battery()                                                                              # Getting the battery level of the Tello.
            print(f"-- PRE LAUNCH --\nBattery Level: {bat}/100")                                                # Getting the battery level of the Tello.
            if isinstance(bat, int) and bat < 15:
                print("Battery too low (<15%). Aborting.")
                return
        except Exception as e:
            print(f"Could not get battery level: {e}. Proceeding with caution.")

        me.set_speed(15)                                                                                        # 15 cm/s = slow, safe indoor pace
        me.takeoff()                                                                                            # Take off is auto 80cm from ground.
        time.sleep(2)                                                                                           # Wait for 2 seconds.

        me.move_up(50)                                                                                          # Move up 50cm. Total = 1.3m (130cm)
        getInfo(me)
        time.sleep(2)                                                                                           # Wait for 2 seconds.

        me.move_down(30)                                                                                        # Move down so we can be approximately 1m from ground. Total = 1m (100cm)
        getInfo(me)
        time.sleep(1)                                                                                           # Pause for effect.

        me.move_right(50)                                                                                       # Moving 50cm to the right. 50cm from origin.
        me.move_up(20)                                                                                          # Move up 20cm. Total = 1.2m (120cm)
        getInfo(me)
        time.sleep(2)                                                                                           # Wait for 2 seconds.

        me.move_left(100)                                                                                       # Move 100cm to the left. 50cm from origin to the left.
        me.move_down(10)                                                                                        # Move down 10cm. Total = 1.1m (110cm)
        getInfo(me)
        time.sleep(2)                                                                                           # Wait for 2 seconds.

        me.move_right(50)                                                                                       # Move back to the origin.
        getInfo(me)
        time.sleep(2)                                                                                           # Wait for 2 seconds.

        print("Preparing to land...")
        time.sleep(2)                                                                                           # Wait for 2 seconds.
        me.land()
        getInfo(me)

        print("Landed Successfully")
        try:
            print(f"-- POST LANDING --\nBattery Level: {me.get_battery()}/100")                                       # Getting the battery level of the Tello.
        except Exception as e:
            print(f"Could not get battery level: {e}.")

    except Exception as e:
        print("Error:", e)                                                                                            # Print any error that occurs during the connection attempt.
        try:
            me.land()
        except:
            try:
                me.emergency()
            except:
                pass

    finally:
        try:
            me.end()                                                                                            # Ending the Tello object connection.
        except:
            pass

if __name__ == "__main__":
    main()
