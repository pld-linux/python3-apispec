#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Pluggable API specification generator
Summary(pl.UTF-8):	Generator specyfikacji API z obsługą wtyczek
Name:		python3-apispec
Version:	6.9.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/apispec/
Source0:	https://files.pythonhosted.org/packages/source/a/apispec/apispec-%{version}.tar.gz
# Source0-md5:	ccd10389ca94fe9acc7ff542b9bf1fa2
URL:		https://pypi.org/project/apispec/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-flit_core < 4
BuildRequires:	python3-modules >= 1:3.10
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.10
BuildRequires:	python3-marshmallow >= 3.18.0
BuildRequires:	python3-openapi-spec-validator >= 0.7.2
BuildRequires:	python3-packaging >= 21.3
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-PyYAML >= 6.0.3
BuildRequires:	python3-marshmallow >= 3.18.0
BuildRequires:	python3-packaging >= 21.3
BuildRequires:	python3-sphinx_issues >= 5.0.1
BuildRequires:	python3-sphinx_rtd_theme >= 3.0.2
BuildRequires:	sphinx-pdg-3 >= 8.2.3
%endif
Requires:	python3-modules >= 1:3.10
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
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE README.rst SECURITY.md
%{py3_sitescriptdir}/apispec
%{py3_sitescriptdir}/apispec-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
