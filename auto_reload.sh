#!/bin/bash
cd ~/new_vision/data/src
uvicorn app:app --host '0.0.0.0' --port 8080