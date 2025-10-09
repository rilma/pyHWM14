# Install python sources

python_sources = ['__init__.py']

py.install_sources(
    python_sources,
    subdir: 'pyhwm2014'
)

# Install additional data sources

data_dir = 'data/'
install_dir = py.get_install_dir() / 'pyhwm2014'

data_sources = files(
    data_dir / 'dwm07b104i.dat',
    data_dir / 'gd2qd.dat',
    data_dir / 'hwm123114.bin')

install_data(
    data_sources,
    install_dir: install_dir / 'data'
)
