# Install python sources

python_sources = ['__init__.py']

py.install_sources(
    python_sources,
    subdir: 'pyhwm14'
)

# Install additional data sources

data_dir = 'data/'

data_sources = [
    data_dir / 'dwm07b104i.dat',
    data_dir / 'gd2qd.dat',
    data_dir / 'hwm123114.bin']

py.install_sources(
    data_sources,
    subdir: 'pyhwm14/data/'
)
