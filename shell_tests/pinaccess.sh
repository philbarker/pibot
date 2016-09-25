#!/bin/bash
for pin in 17 18 22 24 27; do
  gpio write $pin 0
  gpio export $pin out
done
gpio export 23 in
