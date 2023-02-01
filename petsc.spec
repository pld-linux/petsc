#
# Conditional build:
%bcond_with	mpi	# MPI support
#
Summary:	PETSc - Portable, Extensible Toolkit for Scientific Computation
Summary(pl.UTF-8):	PETSc - przenośny, rozszerzalny zestaw narządzi do obliczeń naukowych
Name:		petsc
Version:	3.18.3
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/%{name}-%{version}.tar.gz
# Source0-md5:	db8de65fea494b42097f29f17f5be4fc
#Patch0:	%{name}-what.patch
URL:		https://petsc.org/release/
BuildRequires:	gcc-fortran
BuildRequires:	lapack-devel
BuildRequires:	libstdc++-devel
%if %{with mpi}
BuildRequires:	mpich-devel
BuildRequires:	mpich-c++-devel
BuildRequires:	mpich-fortran-devel
%endif
BuildRequires:	python3 >= 1:3.4
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Portable, Extensible Toolkit for Scientific Computation (PETSc),
is a suite of data structures and routines for the scalable (parallel)
solution of scientific applications modeled by partial differential
equations. It employs the Message Passing Interface (MPI) standard for
all message-passing communication.

%description -l pl.UTF-8
PETSc (Portable, Extensible Toolkit for Scientific Computation, tj.
przenośny, rozszerzalny zestaw narządzi do obliczeń naukowych) to
zbiór struktur danych i procedur do skalowalnego (zrównoleglonego)
rozwiązywania zastosowań naukowych modelowanych za pomocą równań
różniczkowych. Wykorzystuje standard MPI (Message Passing Interface)
do komunikacji związanej z przesyłaniem wiadomości.

%package devel
Summary:	Header files for PETsc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PETsc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lapack-devel
Requires:	libstdc++-devel
Requires:	xorg-lib-libX11-devel

%description devel
Header files for PETsc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PETsc.

%prep
%setup -q
#%patch0 -p1

%build
CC="%{__cc}" \
CXX="%{__cc}" \
CFLAGS="%{rpmcflags}" \
CPPFLAGS="%{rpmcppflags}" \
CXXFLAGS="%{rpmcxxflags}" \
LDFLAGS="%{rpmldflags}" \
%{__python3} configure \
	-CC="%{__cc}" \
	-CXX="%{__cxx}" \
	-LDFLAGS="%{rpmldflags}" \
	-prefix=%{_prefix} \
	-with-debugging=0 \
	-with-fortran-bindings=1 \
	%{!?with_mpi:-with-mpi=0}

%{__make} all-local \
	PETSC_ARCH=arch-linux-c-opt \
	PETSC_DIR=$(pwd) \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PETSC_ARCH=arch-linux-c-opt \
	PETSC_DIR=$(pwd) \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -i -e 's,^libdir=.*,libdir=${prefix}/%{_lib},' $RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# TODO: package reasonable part of this stuff (in proper place)
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/petsc/{bin,conf} \
	$RPM_BUILD_ROOT%{_datadir}/petsc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpetsc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpetsc.so.3.18

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpetsc.so
%{_includedir}/petsc
%{_includedir}/petsc*.h
%{_includedir}/petsc*.hpp
%{_includedir}/mpiuni.mod
%{_includedir}/petsc*.mod
%{_pkgconfigdir}/PETSc.pc
%{_pkgconfigdir}/petsc.pc
