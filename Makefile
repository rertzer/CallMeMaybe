
install:
	export UV_CONCURRENT_DOWNLOADS=1 \
	export UV_CONCURRENT_INSTALLS=1 \
	export UV_CONCURRENT_BUILDS=1 \
	uv sync	 

	@echo "Call Me Maybe Installed" 


export:
	export UV_CACHE_DIR=/tmp/uv/cache
	export UV_TOOL_DIR=/tmp/uv/tools
	export UV_TOOL_BIN_DIR=/tmp/uv/bin
	export UV_PYTHON_INSTALL_DIR=/tmp/uv/python
