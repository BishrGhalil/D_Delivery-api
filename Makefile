run:
	python D_Delivery.py

clean:
	find D_Delivery -depth -name __pycache__ -type d -exec rm -r -- {} \;
	find -depth -name "*.log" -type f -exec rm -rf -- {} \;
	rm -rf dist build D_Delivery.egg-info
