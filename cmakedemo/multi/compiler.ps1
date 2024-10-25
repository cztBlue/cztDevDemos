Remove-Item ".\biuld\*" -Recurse
cd biuld
cmake -G "MinGW Makefiles"..
make
cd ..


