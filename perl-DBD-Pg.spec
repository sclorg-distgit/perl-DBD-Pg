%{?scl:%scl_package perl-DBD-Pg}

Name:           %{?scl_prefix}perl-DBD-Pg
Summary:        A PostgreSQL interface for perl
Version:        3.5.3
Release:        4%{?dist}
# Pg.pm, README:    Points to directory which contains GPLv2+ and Artistic
# other files:      Same as Perl (GPL+ or Artistic)
License:        GPLv2+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/T/TU/TURNSTEP/DBD-Pg-%{version}.tar.gz 
# Adjust tests to postgresql-8.4 that does not support client_encoding option
# in connect string, CPAN RT#116179
Patch0:         DBD-Pg-3.5.3-compatible-client_encoding-against-postgresql-8.4.patch
URL:            http://search.cpan.org/dist/DBD-Pg/

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-devel
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(vars)
BuildRequires:  %{?scl_prefix}perl(warnings)
BuildRequires:  postgresql-devel >= 7.4
# Run-time:
# Prevent bug #443495
BuildRequires:  %{?scl_prefix}perl(DBI) >= 1.614
BuildRequires:  %{?scl_prefix}perl(DynaLoader)
BuildRequires:  %{?scl_prefix}perl(Exporter)
BuildRequires:  %{?scl_prefix}perl(version)
# Tests:
BuildRequires:  %{?scl_prefix}perl(charnames)
BuildRequires:  %{?scl_prefix}perl(constant)
BuildRequires:  %{?scl_prefix}perl(Cwd)
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(POSIX)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.88
BuildRequires:  %{?scl_prefix}perl(Test::Simple)
BuildRequires:  %{?scl_prefix}perl(Time::HiRes)
BuildRequires:  %{?scl_prefix}perl(utf8)
BuildRequires:  postgresql-server
# Optional tests:
BuildRequires:  %{?scl_prefix}perl(Encode)
BuildRequires:  %{?scl_prefix}perl(File::Temp)

Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(DBI) >= 1.614

# Missed by the find provides script:
Provides:       %{?scl_prefix}perl(DBD::Pg) = %{version}

%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_from_provides /^%{?scl_prefix}perl(DBD::Pg)$/d
%filter_from_requires /^%{?scl_prefix}perl(DBI)$/d
%?perl_default_filter
}
%else
# RPM 4.9 style
%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(DBD::Pg\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\(DBI\\)$
%endif

%description
DBD::Pg is a Perl module that works with the DBI module to provide access
to PostgreSQL databases.

%prep
%setup -q -n DBD-Pg-%{version}
%patch0 -p1

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=$RPM_BUILD_ROOT%{?scl:'}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
# Full test coverage requires a live PostgreSQL database (see the README file)
#export DBI_DSN=dbi:Pg:dbname=<database>
#export DBI_USER=<username>
#export DBI_PASS=<password>
# If variables undefined, package test will create it's own database.
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc Changes README README.dev TODO
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/Bundle/DBD/Pg.pm
%{_mandir}/man3/*.3*

%changelog
* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 3.5.3-4
- SCL

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.3-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 02 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.3-1
- 3.5.3 bump

* Wed Sep 30 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.2-1
- 3.5.2 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.1-2
- Perl 5.22 rebuild

* Wed Feb 18 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.1-1
- 3.5.1 bump

* Wed Feb 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.5.0-1
- 3.5.0 bump
- Remove tests sub-package, tests don't work without Makefile

* Mon Sep 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.2-1
- 3.4.2 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-2
- Perl 5.20 rebuild

* Fri Aug 22 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-1
- 3.4.1 bump

* Tue Aug 19 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.0-1
- 3.4.0 bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.3.0-1
- 3.3.0 bump

* Mon May 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.2.1-1
- 3.2.1 bump

* Mon Apr 14 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.1.1-1
- 3.1.1 bump

* Wed Feb 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.0-1
- 3.0.0 bump

* Wed Jan 29 2014 Petr Pisar <ppisar@redhat.com> - 2.19.3-6
- Adapt to changes in Postgres 9.3 (bug #1058723)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.19.3-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 2.19.3-2
- Specify all dependencies
- Move testme.tmp.pl to tests sub-package

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 2.19.3-1
- 2.19.3 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 2.19.2-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Marcela Mašláňová <mmaslano@redhat.com> 2.19.2-1
- bump to 2.19.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-3
- Perl mass rebuild

* Mon Apr  4 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-2
- add requirement for test file

* Tue Mar 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.18.0-1
- update to 2.18.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Marcela Mašláňová <mmaslano@redhat.com> 2.17.2-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (2.17.2)

* Thu Sep 30 2010 Petr Sabata <psabata@redhat.com> - 2.17.1-3
- Fixing BuildRequires (perl-version, Test::More)
- Re-enabling tests
- Resolves: rhbz#633108

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.17.1-2
- Mass rebuild with perl-5.12.0

* Tue Apr 27 2010 Petr Pisar <ppisar@redhat.com> - 2.17.1-1
- upstream released 2.17.1
- GPL+ license corrected to GPLv2+
- enable and run %%check in C locale

* Wed Jan 27 2010 Stepan Kasal <skasal@redhat.com> - 2.15.1-3
- drop patch that was upstreamed long ago (<=2.8.7)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.15.1-2
- rebuild against perl 5.10.1

* Thu Sep 24 2009 Stepan Kasal <skasal@redhat.com> - 2.15.1-1
- new upstream version
- add versioned provide (#525502)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 2.13.1-2
- rebuild against perl-DBI-1.609

* Mon May  4 2009 Stepan Kasal <skasal@redhat.com> - 2.13.1-1
- new upstream release, also fixes #498899

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Stepan Kasal <skasal@redhat.com> - 2.11.6-2
- fix the source URL

* Fri Dec  5 2008 Marcela Mašláňová <mmaslano@redhat.com> - 2.11.6-1
- update

* Fri Oct 31 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.11.2-1
- update to 2.11.2

* Fri Aug 29 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.10.0-1
- update to 2.10.0

* Mon Aug 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.9.2-1
- update to 2.9.2

* Mon Jul 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 2.8.7-1
- new version has Pg.pm twice in two locations
- update

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-9
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.49-8
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-7
- rebuild for new perl

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-6
- Apply changes from package review.
- Resolves: bz#226252

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.49-5.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-5
- Fix license tag
- Add %%doc
- Remove explicit Provides: %{?scl_prefix}perl(DBD::Pg) = %%{version}
- Other cleanups

* Tue Jul 17 2007 Robin Norwood <rnorwood@redhat.com> - 1.49-4
- Fix summary

* Tue Dec 05 2006 Robin Norwood <rnorwood@redhat.com> - 1.49-3
- rebuild for new version of postgres.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.49-2
- rebuild

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 1.49-1
- Upgrade to upstream version 1.49

* Wed Apr 12 2006 Jason Vas Dias <jvdias@redhat.com> - 1.48-1
- Upgrade to upstream version 1.48

* Wed Mar 22 2006 Jason Vas Dias <jvdias@redhat.com> - 1.47-1
- Upgrade to upstream version 1.47

* Wed Mar 08 2006 Jason Vas Dias <jvdias@redhat.com> - 1.45-1
- Upgrade to upstream version 1.45

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.43-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.43-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.43-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Nov 03 2005 Florian La Roche <laroche@redhat.com>
- make sure correct Provides: are generated for this module

* Tue Jun 28 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.43-1
- Update to 1.43 (corrects #156840).

* Thu May 19 2005 Warren Togami <wtogami@redhat.com> - 1.41-2
- Disable gcc optimization to workaround broken placeholders (#156840)

* Wed  Apr 13 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.41-1
- Update to 1.41.
- Updated the requirements versions.
- Specfile cleanup. (#154203)

* Wed Apr 13 2005 Joe Orton <jorton@redhat.com> 1.40-2
- rebuild for new libpq soname

* Thu Mar 31 2005 Warren Togami <wtogami@redhat.com> 1.40-1
- 1.40

* Tue Oct 12 2004 Chip Turner <cturner@redhat.com> 1.32-1
- bugzilla: 127755, update to 1.32

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.31-2
- rebuild

* Thu Dec 11 2003 Chip Turner <cturner@redhat.com> 1.31-1
- update to 1.31

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 1.22-1
- move to upstream 1.22

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Mon Jan 13 2003 Chip Turner <cturner@redhat.com>
- update to 1.21

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use internal rpm dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-5
- Rebuild

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-4
- Rebuild, to fix #66304

* Wed Jun  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-3
- Integrate with newer perl

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.13-1
- 1.13

* Fri Feb 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-8
- Rebuild

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-7
- Rebuild

* Thu Jan 31 2002 Tim Powers <timp@redhat.com>
- rebuild to solve more deps

* Tue Jan 29 2002 Bill Nottingham <notting@redhat.com> 1.01-5
- rebuild (dependencies)

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.01-2
- Rebuild

* Sun Jul  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.01 bugfix release ("bytea" coredumped with values outside 0...127)
- Add perl-DBI and perl to BuildRequires (they were just in Requires: previously)

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.00
- change group to Applications/Databases from Applications/CPAN

* Tue May  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.98, for postgresql-7.1
- add doc files
- cleanups

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- First cut
