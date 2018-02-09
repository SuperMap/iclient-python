#!/bin/bash
cp ../../jupyter/dist/iclientpy-*.whl ./
docker build -t iclientpy/jupyterhub .