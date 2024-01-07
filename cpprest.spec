%global __requires_exclude cmake\\(winhttppal\\)|cmake\\(WINHTTPPAL\\)|cmake\\(unofficial-brotli\\)

%define libname		%mklibname %{name}
%define devname		%mklibname %{name} -d

Summary:	C++ REST library
Name:		cpprest
Version:	2.10.18
Release:	1
License:	MIT
Group:		System/Libraries
URL:		https://github.com/microsoft/cpprestsdk
Source0:	https://github.com/microsoft/cpprestsdk/archive/refs/tags/v%{version}/cpprestsdk-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	boost-devel
BuildRequires:	cmake(websocketpp)
BuildRequires:	pkgconfig(libbrotlidec)
BuildRequires:	pkgconfig(libbrotlienc)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)

%description
The C++ REST SDK is a Microsoft project for cloud-based client-server
communication in native code using a modern asynchronous C++ API design. This
project aims to help C++ developers connect to and interact with services.

Also known as Casablanca.

#----------------------------------------------------------------------------

%package -n	%{libname}
Summary:	C++ Rest library
Group:		System/Libraries

%description -n	%{libname}
The C++ REST SDK is a Microsoft project for cloud-based client-server
communication in native code using a modern asynchronous C++ API design. This
project aims to help C++ developers connect to and interact with services.

%files -n %{libname}
%license license.txt
%doc CONTRIBUTORS.txt
%{_libdir}/libcpprest.so.*

#----------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development package for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The C++ REST SDK is a Microsoft project for cloud-based client-server
communication in native code using a modern asynchronous C++ API design. This
project aims to help C++ developers connect to and interact with services.

Header files for development with %{name}.

%files -n %{devname}
%license license.txt
%doc CONTRIBUTORS.txt
%{_includedir}/%{name}/
%{_includedir}/pplx/
%{_libdir}/libcpprest.so
%{_libdir}/cmake/cpprestsdk/
%{_libdir}/pkgconfig/%{name}.pc

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n cpprestsdk-%{version}

# Remove bundled sources of websocketpp
rm -r Release/libs
# Remove file ThirdPartyNotices.txt, which is associated to websocketpp
rm ThirdPartyNotices.txt

%build
export LDFLAGS="%{ldflags} -Wl,--as-needed"
# FIXME: clang falis dut to zblib
export CC=gcc
export CXX=g++

%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCPPREST_EXCLUDE_BROTLI:BOOL=OFF \
	-DWERROR:BOOL=OFF \
	-GNinja
%ninja_build

%install
%ninja_install -C build

# pkgconfig file
install -d %{buildroot}%{_libdir}/pkgconfig
cat << EOF > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: cloud-based client-server communication
URL: %{url}
Version: %{version}
Libs: -L%{_libdir} -lcpprest
Cflags: -I%{_includedir}/cpprest -I%{_includedir}/pplx
EOF

