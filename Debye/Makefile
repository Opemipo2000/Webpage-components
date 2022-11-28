# Configuration variables

# ARCHIVE="fdtd-3d_`date +%F`.tar.bz2"
# ls
OUT_DIR=./
# LIBFILE="libfdtd.a"
# LIBNAME="fdtd"
# CFLAGS=-mcmodel=medium -O3 -frecord-marker=4 -fbounds-check
 CFLAGS= #-O3 #-frecord-marker=4 -fbounds-check

CC=gfortran
objects =  sgesv.o xerbla.o ilaenv.o lsame.o iparmq.o ieeeck.o slamch.o isamax.o scabs1.o sgetrf.o sgetrs.o sgetf2.o slaswp.o strsm.o sgemm.o sswap.o sger.o sscal.o





#------------------------------------------------------------------------------

Debye : Debye.F90 ${objects} 
	${CC}  ${CFLAGS} -o Debye ${objects} $@.F90



sgesv.o :  sgesv.f
	${CC} -O3 -c sgesv.f


sgemm.o :  sgemm.f
	${CC} -O3 -c sgemm.f


sswap.o :  sswap.f
	${CC} -O3 -c sswap.f


sger.o :  sger.f
	${CC} -O3 -c sger.f

sscal.o :  sscal.f
	${CC} -O3 -c sscal.f


strsm.o :  strsm.f
	${CC} -O3 -c strsm.f


sgetf2.o :  sgetf2.f
	${CC} -O3 -c sgetf2.f


slaswp.o :  slaswp.f
	${CC} -O3 -c slaswp.f

sgetrf.o :  sgetrf.f
	${CC} -O3 -c sgetrf.f


sgetrs.o :  sgetrs.f
	${CC} -O3 -c sgetrs.f

xerbla.o :  xerbla.f
	${CC} -O3 -c xerbla.f

ilaenv.o : ilaenv.f
	${CC} -O3 -c ilaenv.f

slamch.o : slamch.f
	${CC} -O3 -c slamch.f


lsame.o : lsame.f
	${CC} -O3 -c lsame.f

isamax.o : isamax.f
	${CC} -O3 -c isamax.f

iparmq.o : iparmq.f
	${CC} -O3 -c iparmq.f 

ieeeck.o : ieeeck.f
	${CC} -O3 -c ieeeck.f 

scabs1.o : scabs1.f
	${CC} -O3 -c scabs1.f


#------------------------------------------------------------------------------

run:
	./Debye

clean:
	rm Debye *.o *~ *.txt 

cleantxt:
	rm *~ *.txt 

