# pyHWM14 Development Roadmap

This document outlines the planned development direction for pyHWM14. Items are organized by priority and expected timeline.

## This Version (1.1.x)

- ✅ Python 3.13 support  
- ✅ Type hints throughout codebase
- ✅ Comprehensive test coverage
- ✅ Enhanced CI/CD pipeline with linting and security checks

## Next Release (1.2.0) - Q2 2026

### Performance Improvements
- Vectorize core wind calculations for 20-30% speedup
- Add optional Numba JIT compilation for intensive computations
- Profile memory usage and optimize data structures

### New Features
- **Interpolation methods** - Smooth wind profiles between points
- **Batch processing** - Calculate winds for multiple locations in one call
- **Output formats** - Export to NetCDF, HDF5, or CSV

### Documentation
- Create Sphinx documentation site with examples
- Add comprehensive API reference
- Create Jupyter notebook tutorials
- Add "Getting Started" video guide

### Developer Experience
- Publish on Conda-Forge for conda installation
- Add Docker container for reproducibility
- Pre-commit hook templates for contributors
- GitHub Discussions enabled for Q&A

## Future Releases (1.3.0+)

### Model Updates
- Support for HWM21 model (when available)
- Historical model versions (HWM07, HWM14, future versions)
- Ensemble/uncertainty estimates if available

### Advanced Features
- **Real-time data** - Fetch geomagnetic indices automatically
- **Visualization** - Built-in plotting with geographical data
- **ML Integration** - ML-based anomaly detection for wind extremes
- **Web API** - RESTful interface for remote calculations

### Community
- Partner with atmospheric science research groups
- Academic publications showcasing use cases
- Stale branch of model code for educational purposes

### Research Extensions
- Uncertainty quantification framework
- Model comparison tools
- Integration with other atmospheric models

## Far Future (2.0.0+)

### Major Redesign
- Plugin system for different wind models
- Support for multiple atmospheric properties (temperature, density, etc.)
- C/C++ kernel with Python bindings for extreme performance
- WebAssembly version for browser-based calculations

### Broader Ecosystem
- Integration with GIS tools (GDAL, GeoPandas)
- Climate modeling framework compatibility
- Real-time operational forecasting pipeline

## Known Limitations & Future Fixes

| Issue | Impact | Planned Fix | Timeline |
|-------|--------|-------------|----------|
| P3.12 deprecated (< 3.13) | Build compatibility | Drop with 2.0.0 | 2027+ |
| Single Python version tested | CI coverage | Matrix test 3.13+ | 1.2.0 |
| Limited example code | New user friction | Add tutorials | 1.2.0 |
| No online documentation | Discoverability | Sphinx docs | 1.2.0 |
| Windows support unclear | User access | Explicit CI testing | 1.3.0 |

## Community Contributions Welcome

These areas are great for community involvement:

- 🐛 **Bug reports** - Any platform (macOS, Windows, Linux)
- 📖 **Documentation** - Examples, tutorials, translations
- 🧪 **Testing** - Expand test coverage, edge cases
- ⚙️ **Performance** - Profiling and optimization
- 🔌 **Extensions** - Integration with other tools
- 💡 **Ideas** - Feature requests and enhancements

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get involved!

## Feedback & Suggestions

Have ideas? Please:
1. **Check existing issues** to avoid duplicates
2. **Create a Discussion** on GitHub for ideas (not PRs yet)
3. **File an Issue** for bugs with reproducible examples
4. **Submit a PR** if you want to contribute!

---

**Last Updated:** February 15, 2026  
**Next Review:** Q2 2026

Would you like to discuss any of these priorities?
