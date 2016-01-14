%{?scl:%scl_package perl-DBD-Pg}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}perl-DBD-Pg
Summary:        A PostgreSQL interface for perl
Version:        2.19.3
Release:        5.sc1%{?dist}
License:        GPLv2+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/T/TU/TURNSTEP/DBD-Pg-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/DBD-Pg/

BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(constant)
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  postgresql-devel >= 7.4
# Run-time:
# Prevent bug #443495
BuildRequires:  %{?scl_prefix}perl(DBI) >= 1.607
BuildRequires:  %{?scl_prefix}perl(Exporter)
BuildRequires:  %{?scl_prefix}perl(version)
# Tests:
# The macro %%tests_req was defined at RHEL 7.
# It is possible the build environment was not set properly in case the
# %%{?scl}tests_req is not defined during installing BR (mainly on RHEL 6)
BuildRequires:  %{?scl_prefix}perl(Cwd)
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.61
BuildRequires:  %{?scl_prefix}perl(Test::Simple)
BuildRequires:  %{?scl_prefix}perl(Time::HiRes)
BuildRequires:  postgresql-server
# Optional tests:
BuildRequires:  %{?scl_prefix}perl(Encode)
BuildRequires:  %{?scl_prefix}perl(File::Temp)
# test sub-package requirements
%tests_subpackage_requires %{?scl_prefix}perl(Carp)
%tests_subpackage_requires %{?scl_prefix}perl(Data::Peek)
%tests_subpackage_requires %{?scl_prefix}perl(DBD::Pg)
%tests_subpackage_requires %{?scl_prefix}perl(DBI)
%tests_subpackage_requires %{?scl_prefix}perl(File::Spec)
%tests_subpackage_requires %{?scl_prefix}perl(lib)
%tests_subpackage_requires %{?scl_prefix}perl(YAML)

%{?scl:%global perl_version %(scl enable %{scl} 'eval "`%{__perl} -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`%{__perl} -V:version`"; echo $version)}
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:       %{?scl_prefix}perl(DBI) >= 1.52

# Missed by the find provides script:
Provides:       %{?scl_prefix}perl(DBD::Pg) = %{version}

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(DBD::Pg\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\(DBI\\)$
%{?perl_default_subpackage_tests}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /perl(DBD::Pg)\s*$/d
%filter_from_requires /perl(DBI)\s*$/d
%filter_setup
%endif

%description
DBD::Pg is a Perl module that works with the DBI module to provide access
to PostgreSQL databases.

%prep
%setup -q -n DBD-Pg-%{version}
# Move testme.tmp.pl into tests sub-package
mv testme.tmp.pl t/
sed -i -e '/^testme.tmp.pl$/ s/^/t\//' MANIFEST
sed -i -e '1 s/#!.*//' t/testme.tmp.pl

%build
%{?scl:scl enable %{scl} '}
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
%{?scl:'}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
%{?scl:"}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
# Full test coverage requires a live PostgreSQL database (see the README file)
#export DBI_DSN=dbi:Pg:dbname=<database>
#export DBI_USER=<username>
#export DBI_PASS=<password>
# If variables undefined, package test will create it's own database.
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}

%files
%doc Changes README README.dev TODO
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/Bundle/DBD/Pg.pm
%{_mandir}/man3/*.3*


%changelog
* Thu Feb 13 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.19.3-5
- Updated conditions to work properly for non-RHEL systems
- Resolves: rhbz#1064855

* Tue Jan 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.19.3-4
- Add building of tests sub-package
- Resolves: rhbz#1049366

* Wed Nov 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.19.3-3
- Fix MODULE_COMPAT BR

* Tue Sep 24 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.19.3-2
- Specify all dependencies
- Resolves: rhbz#1009514

* Mon Apr 08 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.19.3-1
- SCL package - initial import
