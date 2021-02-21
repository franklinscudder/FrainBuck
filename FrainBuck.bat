@echo off
IF NOT "%1"=="" (
    python interpreter.py --file %1
    )	ELSE (
	python interpreter.py
	)
