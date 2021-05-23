%global nspr_version 4.30
Name:          nss
Version:       3.65
Release:       57
URL:           https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS/
Source0:       https://ftp.mozilla.org/pub/security/nss/releases/NSS_3_65_RTM/src/nss-3.65.tar.gz
Source1:       nss.pc.in
Source2:       nss-config.in
Summary:       Network Security Services
Group:         Development/Tools
License:       MPL-2.0
BuildRequires: pkg-config
BuildRequires: pkgconfig(nspr) >= %{nspr_version}
BuildRequires: nspr-lib32
BuildRequires: pkgconfig(32nspr)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(32sqlite3)
BuildRequires: zlib-dev
BuildRequires: zlib-dev32
BuildRequires: gcc-dev32
BuildRequires: gcc-libgcc32
BuildRequires: gcc-libstdc++32
BuildRequires: glibc-dev32
BuildRequires: glibc-libc32

Requires:      nss-lib
Requires:      nss-bin
Requires:      nspr >= %{nspr_version}
Requires:      p11-kit

Patch1: 0001-Skip-dbtest-that-fails-with-sqlite-3.34.0.patch

%description
Network Security Services (NSS) is a set of libraries designed
to support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME,
X.509 v3 certificates, and other security standards.  See:
http://www.mozilla.org/projects/security/pki/nss/overview.html

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

%package dev
Summary:        Network (Netscape) Security Services development files
Group:          Development/Libraries
Requires:       nspr-dev
Requires:       nss-lib

%description dev
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2 and v3,
TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards.


%package lib
Summary:        NSS Libraries
Group:          Security/Crypto Libraries

%description lib
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2 and v3,
TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards.

%package lib32
Summary:        NSS Libraries
Group:          Security/Crypto Libraries

%description lib32
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2 and v3,
TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards.


%package bin
Summary:       Tools for developing, debugging, and managing NSS applications
Group:         Security/Crypto Libraries
Requires:      nss-lib

%description bin
The NSS Security Tools allow developers to test, debug, and manage
applications that use NSS.

%prep
%setup -q -n nss-%{version}/nss
%patch1 -p1
pushd ..
cp -a nss build32
popd

%build
export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1
export CC=gcc
export USE_64=1
export NSS_USE_SYSTEM_SQLITE=1
export NSS_ENABLE_WERROR=0
export USE_SYSTEM_ZLIB=1
export FREEBL_NO_DEPEND=1
export NSS_ENABLE_TLS_1_3=1
export MAKE_FLAGS="BUILD_OPT=1 NSS_ENABLE_ECC=1"
export CFLAGS="$CFLAGS -Wno-error"
export CXXFLAGS="$CFLAGS -Wno-error"

make -O %{?_smp_mflags}

pushd ../build32

export CC=gcc
unset USE_64
export USE_32=1
export NSS_USE_SYSTEM_SQLITE=1
export NSS_ENABLE_WERROR=0
export USE_SYSTEM_ZLIB=1
export FREEBL_NO_DEPEND=1
export NSS_ENABLE_TLS_1_3=1
export MAKE_FLAGS="BUILD_OPT=1 NSS_ENABLE_ECC=1"
export CFLAGS="$CFLAGS -Wno-error -m32 -mstackrealign"
export CXXFLAGS="$CFLAGS -Wno-error -m32 -mstackrealign"
export LDFLAGS="$LDFLAGS -m32 -mstackrealign"

make -O %{?_smp_mflags}

popd

%install

export FREEBL_NO_DEPEND=1
export USE_64=1
export CFLAGS="$CFLAGS -Wno-error"
export CXXFLAGS="$CFLAGS -Wno-error"

mkdir -p %{buildroot}/usr/lib64
mkdir -p %{buildroot}/usr/lib32
mkdir -p %{buildroot}/usr/lib64/pkgconfig
mkdir -p %{buildroot}/usr/lib64/nss
mkdir -p %{buildroot}/usr/include/nss3
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/sbin

# Work inside dist where binaries are generated
pushd ../dist/Linux*_x86_64_gcc_glibc_PTH_64_DBG.OBJ

# Remove static libraries
rm -fr lib/*.a lib64/*.a

# Copy headers
cp -rL ../public/nss/*.h %{buildroot}/usr/include/nss3

# Copy dynamic libraries
cp -L lib/libnss3.so \
      lib/libnssdbm3.so \
      lib/libnssdbm3.chk \
      lib/libnssutil3.so \
      lib/libsmime3.so \
      lib/libsoftokn3.so \
      lib/libsoftokn3.chk \
      lib/libssl3.so \
      %{buildroot}/usr/lib64

# Copy libfreebl libraries
cp -L lib/libfreebl3.so \
      lib/libfreebl3.chk \
      %{buildroot}/usr/lib64

# Copy tools
cp -L bin/certutil \
      bin/cmsutil \
      bin/crlutil \
      bin/modutil \
      bin/pk12util \
      bin/signtool \
      bin/signver \
      bin/ssltap \
      %{buildroot}/usr/bin

# Copy unsupported tools
cp -L bin/atob \
      bin/btoa \
      bin/derdump \
      bin/ocspclnt \
      bin/pp \
      bin/selfserv \
      bin/shlibsign \
      bin/strsclnt \
      bin/symkeyutil \
      bin/tstclnt \
      bin/vfyserv \
      bin/vfychain \
      %{buildroot}/usr/lib64/nss
popd

pushd ../dist/Linux*_x86_gcc_glibc_PTH_DBG.OBJ

# Remove static libraries
rm -fr lib/*.a lib64/*.a lib32/*.a

# Copy dynamic libraries
cp -L lib/libnss3.so \
      lib/libnssdbm3.so \
      lib/libnssdbm3.chk \
      lib/libnssutil3.so \
      lib/libsmime3.so \
      lib/libsoftokn3.so \
      lib/libsoftokn3.chk \
      lib/libssl3.so \
      %{buildroot}/usr/lib32

# Copy libfreebl libraries
cp -L lib/libfreebl3.so \
      lib/libfreebl3.chk \
      %{buildroot}/usr/lib32

popd

# Prepare pkgconfig file
mkdir -p %{buildroot}/usr/lib64/pkgconfig/
sed "s:%%LIBDIR%%:/usr/lib64:g
s:%%VERSION%%:%{version}:g
s:%%NSPR_VERSION%%:%{nspr_version}:g" \
  %{SOURCE1} > %{buildroot}/usr/lib64/pkgconfig/nss.pc

# Prepare nss-config file
NSS_VMAJOR=`cat ./lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat ./lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat ./lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`
cat %{SOURCE2} | sed -e "s,@libdir@,/usr/lib64,g" \
                     -e "s,@prefix@,/usr,g" \
                     -e "s,@exec_prefix@,/usr,g" \
                     -e "s,@includedir@,/usr/include/nss3,g" \
                     -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                     -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                     -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                     > %{buildroot}/usr/bin/nss-config
chmod 755 %{buildroot}/usr/bin/nss-config

%check
pushd tests
export USE_64=1
HOST=127.0.0.1  bash ./all.sh
popd

%clean
rm -fr %{buildroot}

%files lib
%defattr(-,root,root,-)
/usr/lib64/libnss3.so
/usr/lib64/libnssutil3.so
/usr/lib64/libsmime3.so
/usr/lib64/libssl3.so
/usr/lib64/libfreebl3.so
/usr/lib64/libfreebl3.chk
/usr/lib64/libsoftokn3.so
/usr/lib64/libsoftokn3.chk
/usr/lib64/libnssdbm3.so
/usr/lib64/libnssdbm3.chk

%files lib32
%defattr(-,root,root,-)
/usr/lib32/libnss3.so
/usr/lib32/libnssutil3.so
/usr/lib32/libsmime3.so
/usr/lib32/libssl3.so
/usr/lib32/libfreebl3.so
/usr/lib32/libfreebl3.chk
/usr/lib32/libsoftokn3.so
/usr/lib32/libsoftokn3.chk
/usr/lib32/libnssdbm3.so
/usr/lib32/libnssdbm3.chk

%files dev
%defattr(644,root,root,755)
/usr/include/nss3/
/usr/lib64/pkgconfig/*
%attr(755,root,root) /usr/bin/nss-config

%files bin
%defattr(-,root,root)
/usr/bin/*
/usr/lib64/nss/
%exclude /usr/bin/nss-config
