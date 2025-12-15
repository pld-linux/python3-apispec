#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-apispec.spec)

Summary:	Pluggable API specification generator
Summary(pl.UTF-8):	Generator specyfikacji API z obsługą wtyczek
Name:		python-apispec
# keep 2.x here for python2 support
Version:	2.0.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/apispec/
Source0:	https://files.pythonhosted.org/packages/source/a/apispec/apispec-%{version}.tar.gz
# Source0-md5:	4c4ed786cf29d61902886fb8c13c5a78
URL:		https://pypi.org/project/apispec/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.10
BuildRequires:	python-marshmallow >= 2.19.2
BuildRequires:	python-openapi-spec-validator
BuildRequires:	python-prance >= 0.11
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.10
BuildRequires:	python3-marshmallow >= 2.19.2
BuildRequires:	python3-marshmallow < 3
BuildRequires:	python3-openapi-spec-validator
BuildRequires:	python3-prance >= 0.11
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-PyYAML >= 5.1.1
BuildRequires:	python3-marshmallow >= 2.19.5
BuildRequires:	python3-sphinx_issues >= 1.2.0
BuildRequires:	python3-sphinx_rtd_theme >= 0.4.3
BuildRequires:	sphinx-pdg-3 >= 2.1.2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A pluggable API specification generator. Currently supports the
OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>
(f.k.a. the Swagger specification).

%description -l pl.UTF-8
Generator specyfikacji API z obsługą wtyczek. Obecnie obsługuje
OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>
(wcześniej znaną jako Swagger).

%package -n python3-apispec
Summary:	Pluggable API specification generator
Summary(pl.UTF-8):	Generator specyfikacji API z obsługą wtyczek
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-apispec
A pluggable API specification generator. Currently supports the
OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>
(f.k.a. the Swagger specification).

%description -n python3-apispec -l pl.UTF-8
Generator specyfikacji API z obsługą wtyczek. Obecnie obsługuje
OpenAPI Specification <https://github.com/OAI/OpenAPI-Specification>
(wcześniej znaną jako Swagger).

%package apidocs
Summary:	API documentation for Python apispec module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona apispec
Group:		Documentation

%description apidocs
API documentation for Python apispec module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona apispec.

%prep
%setup -q -n apispec-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py_sitescriptdir}/apispec
%{py_sitescriptdir}/apispec-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-apispec
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/apispec
%{py3_sitescriptdir}/apispec-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
