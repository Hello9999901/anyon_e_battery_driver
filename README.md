# Modified from @hoelzro

## Loading the module

You can build the module with a simple `make`, and load it with `insmod`:

    $ sudo insmod ./fake_battery.ko

## Changing battery values via /dev/fake\_battery

You can write values to `/dev/fake_battery` to change the current charging/discharging
and charge levels of the battery:

    $ echo 'charging = 0' | sudo tee /dev/fake_battery # set state to discharging
    $ echo 'charging = 1' | sudo tee /dev/fake_battery # set state to charging
    $ echo 'capacity0 = 77' | sudo tee /dev/fake_battery # set charge on BAT0 to 77%
    $ echo 'capacity1 = 77' | sudo tee /dev/fake_battery # set charge on BAT1 to 77%

