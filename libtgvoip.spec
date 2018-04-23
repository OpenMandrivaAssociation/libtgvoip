Summary: VoIP library for Telegram clients
Name: libtgvoip
Version: 1.0.3
Release: 2

# Libtgvoip shared library - Public Domain.
# Bundled webrtc library - BSD with patented echo cancellation algorithms.
License: Public Domain and BSD
URL: https://github.com/grishka/%{name}

Source0: %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: %{name}-build-fixes.patch

Provides: bundled(webrtc-audio-processing) = 0.3
BuildRequires: pkgconfig(libpulse)
BuildRequires: alsa-oss-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel
BuildRequires: cmake
BuildRequires: gyp

%description
Provides VoIP library for Telegram clients.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%setup -n %{name}-%{version}
%apply_patches

%build
export VOIPVER="%{version}"
#export CC=%{_bindir}/gcc
#export CXX=%{_bindir}/g++
#export CXXFLAGS="%{optflags} -stdlib=libc++ -lpthread -ldl -std=c++11"
export CXXFLAGS="%{optflags} -stdlib=libc++"
%{__python2} %{_bindir}/gyp --format=cmake --depth=. --generator-output=. -Goutput_dir=out -Gconfig=Release %{name}.gyp


pushd out/Release
    %cmake
    %make
popd

%install
# Installing shared library...
mkdir -p "%{buildroot}%{_libdir}"
install -m 0755 -p out/Release/lib.target/%{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.%{version}"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.1.0"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so.1"
ln -s %{name}.so.%{version} "%{buildroot}%{_libdir}/%{name}.so"

# Installing additional development files...
mkdir -p "%{buildroot}%{_includedir}/%{name}/audio"
find . -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name} \;
find audio -maxdepth 1 -type f -name "*.h" -exec install -m 0644 -p '{}' %{buildroot}%{_includedir}/%{name}/audio \;

%files
%license UNLICENSE
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so
