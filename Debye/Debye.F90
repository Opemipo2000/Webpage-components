PROGRAM DebyeParameters
implicit none   
!!DECLARATIONS
COMPLEX, external :: ep_cal_0
REAL, external:: norm
CHARACTER (len=50) , DIMENSION(50) :: TissueNames
CHARACTER (len=50)   :: filePermitivity, fileConductivity,chr
CHARACTER (len=2000) :: line
INTEGER :: permitivityTotalRows, permitivityComments, permitivityDataRows,t,r
INTEGER :: conductivityTotalRows, conductivityComments, conductivityDataRows
INTEGER :: iostatus, i,j,f
INTEGER,DIMENSION(60)::frequency=(/(i,i=1,60)/)!!!!when we need frecuency
!!!!we have to put 'frecuency(i)x1e8
REAL, DIMENSION(60,51) :: permitivity
REAL, DIMENSION(60,51) :: conductivity
REAL::omg(60),omg_0,ep(60,50),sg(60,50),ep_imag(60,50),vector(4)
REAL::ep_infty,Dlt_ep_1,tau_1_nl,sg_0,es,losst1,losst2,tau_1
COMPLEX::ep_cmplx(60,50),ep_cal(60,50),d_ep(60,50),g(60,4)
REAL,PARAMETER::pi=3.1415926536,ep_0=8.854e-12!!physical constant [F/m]
REAL,DIMENSION(4)::dA,A,P,D
REAL::B(4,4), C(4,60)
INTEGER::INFO,N,IPIV(4)
REAL::error
REAL::Q(4,4),PARAMETERS(4,50)
real:: diffpermit,totalpermit,diffconduct,totalconduct


OPEN(UNIT=7,FILE="4parametersfrequency",STATUS='OLD',ACTION='READ',IOSTAT=iostatus)
      read(7, *, iostat=iostatus) chr, sg_0
      read(7, *, iostat=iostatus) chr, es
      read(7, *, iostat=iostatus) chr, ep_infty
      read(7, *, iostat=iostatus) chr, tau_1

 CLOSE (7)

!      write(*,*)  sg_0
!      write(*,*)  es
!      write(*,*)  ep_infty
!      write(*,*)  tau_1_nl
!      write(*,*)  frequency(1)

omg_0=2.0*pi*1e9
Dlt_ep_1 = es-ep_infty
tau_1_nl = tau_1 *omg_0

do i = 1,6000
frequency(1) = i
omg(1) = 2.0*pi*frequency(1)*1e8

losst1=sg_0/omg(1)/ep_0+omg(1)*tau_1*Dlt_ep_1/(1+(omg(1)*tau_1)**2)
losst2 = ep_infty +Dlt_ep_1/(1+ (omg(1)*tau_1)**2 )

! frequency, relative permittivity, conductivity, losstangent
write(20,*)frequency(1)*1e8,real(ep_cal_0(omg(1),omg_0,ep_0,ep_infty,Dlt_ep_1,tau_1_nl,sg_0)),&
-ep_0*omg(1)*aimag(ep_cal_0(omg(1),omg_0,ep_0,ep_infty,Dlt_ep_1,tau_1_nl,sg_0)),losst1/losst2

enddo

END PROGRAM DebyeParameters
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!Define a function we need to calculate epsilon!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
COMPLEX FUNCTION ep_cal_0(omg,omg_0,ep_0,ep_infty,Dlt_ep_1,tau_1_nl,sg_0) 
	
	REAL::ep_infty,Dlt_ep_1,tau_1_nl,sg_0
	REAL::omg,omg_0,ep(60,50),sg(60,50),ep_imag(60,50)  	
	ep_cal_0=(cmplx(ep_infty,0.0)+cmplx(Dlt_ep_1,0.0)/cmplx(1.0,tau_1_nl*omg/omg_0))&
	& +(cmplx(sg_0,0.0)/cmplx(0.0,omg*ep_0))

	END



REAL FUNCTION norm(vector) 
	
	REAL::vector(4)
	norm=sqrt(vector(1)**2+vector(2)**2+vector(3)**2+vector(4)**2)


	END
