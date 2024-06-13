
################################################################
########## Lectura de Archivo y formato ########################
################################################################

filename <- "/Datos/kd.blocks.csv"
column_names <- c('id', 'x', 'y', 'z', 'tonn', 'blockvalue', 'destination', 'CU', 'process_profit')
a <- read.csv(filename, header = FALSE, col.names = column_names, sep=' ')
a <- na.omit(a)
a <- a[, c('x', 'y', 'z', 'CU')]

################################################################
################################################################
################################################################

hist(a$CU)


###########################################################################
################# Transformacion de los datos (Box-cox) ###################
###########################################################################


# La siguiente transformacion se utiliza para cumplir con la hipotesis del
# Box-Cox, de ser estrictamente positiva. Ademas dejamos el porcentaje como 
# decimal.

a$C_CU <- (100-a$CU)/100   

hist(a$C_CU)


######################### Para el Box-Cox utilizamos dos metodos ###############

##### 1°METODO, Forma manual : Se debe escoger con la regla del codo

l = seq(-300,300,by=1) 
d=array(data=NA,dim=length(l)) 

for (i in 1:length(l)) { 
  if (l[i] != 0) { 
    tTF = (a$C_CU^l[i]-1)/l[i] 
  } else { 
    tTF = log(a$C_CU) 
  }
  
  d[i] = (mean(tTF) - median(tTF))/IQR(tTF) 
}
plot(l,d^2)

(l[which(d^2==min(d^2))]) 

## 2° METODO, uso de la libreria MASS:

library(MASS)

bc <- boxcox(a$C_CU ~ 1, lambda = seq(-1000, 1000, by = 1))
lambda_optimo <- bc$x[which.max(bc$y)]
print(lambda_optimo)



############################################################
############### Uso de la transformacion Box-Cox ###########
############################################################

a$BC_C_CU<- (a$C_CU^lambda_optimo - 1)/lambda_optimo
hist(a$BC_C_CU)



#######################################################################################
######################## Verificacion de Hipotesis ####################################
#######################################################################################

#Se analiza si existe alguna tendencia lineal en alguna direccion en las tres coordenadas
#Para ello, se da enfasisi en los P-values pequeños

tx <- lm(a$BC_C_CU ~ a$x)
summary(tx)

ty <- lm(a$BC_C_CU ~ a$y)
summary(ty)

tz <- lm(a$BC_C_CU ~ a$z)
summary(tz)

#######################################################################################
#######################################################################################
#######################################################################################


#######################################################################################
############################### Analisis Variografico ##################################
#######################################################################################



############## Variograma empirico ################

#install.packages("gstat")
#install.packages("sp")
library(sp) 
library(gstat) 


coordinates(a) <- ~x+y+z

summary(a)

# El siguiente vector representa los límites superiores de las clases de distancia de retardo (lags) para el cálculo del variograma
bu = c(0.1, 0.5, seq(1,10,1), seq(12,40,2))

############### Asumiendo media constante #################

#Calculo  del variograma empírico clásico de Matheron, 
v.emp.mat <-variogram(BC_C_CU~1, boundaries = bu, a) 
#Calculo del variograma empírico robusto de Cressie y Hawkins (generalmente mas robusto y el que vamos a utilizar)
v.emp.mod<-variogram(BC_C_CU~1, boundaries = bu, a, cressie = TRUE) 


###########################################################

################## Tendendencia en las coordenadas# ##################

#Calculo  del variograma empírico clásico de Matheron, 
v.emp.mat <-variogram(BC_C_CU~x+y+z, boundaries = bu, a) 
#Calculo del variograma empírico robusto de Cressie y Hawkins (generalmente mas robusto y el que vamos a utilizar)
v.emp.mod<-variogram(BC_C_CU~x+y+z, boundaries = bu, a, cressie = TRUE) 

#####################################################################

###############################

par(mfrow=c(1,2))
plot(v.emp.mat)
plot(v.emp.mod)


################################################



############ Eleccion del variograma Teorico ############


#Podemos ver una lista de los variogramas teoricos disponibles con el comando: vgm()

# Se probaron todos, pero solo se dejaron aquellos con mejores resultados
# Los que incluyen 'Sph', 'Exp' , 'Gau', 'Lin'

v.fit.sph <-  fit.variogram(v.emp.mod, model = vgm("Sph"))
(v.fit.sph)

plot(v.emp.mod, v.fit.sph)


v.fit.exp <-  fit.variogram(v.emp.mod, model = vgm("Exp"))
(v.fit.exp)

plot(v.emp.mod, v.fit.exp)



v.fit.gau <-  fit.variogram(v.emp.mod, model = vgm("Gau"))
(v.fit.gau)

plot(v.emp.mod, v.fit.gau)

v.fit.lin <-  fit.variogram(v.emp.mod, model = vgm("Lin"))
(v.fit.lin)

plot(v.emp.mod, v.fit.lin)


v.fit.mat <-  fit.variogram(v.emp.mod, model = vgm("Mat"))
(v.fit.mat)



### Para saber cual es el que mejor se acerca utilizaremos la suma de las distancias al cuadrado 


(sse.sph <- attr(v.fit.sph,"SSErr"))
(sse.exp <- attr(v.fit.exp,"SSErr"))
(sse.gau <- attr(v.fit.gau,"SSErr"))
(sse.lin <- attr(v.fit.lin,"SSErr"))


#Se concluye con el 'gau', 'lin, y 'sph' son muy parecidas.

##############################################################################
##############################################################################
##############################################################################






##############################################################################
####################### Kriging #######################################
##############################################################################



media_conocida <- mean(a$BC_C_CU, na.rm = TRUE)


# Crear la grilla de destino
xdir <- seq(floor(min(a$x)), ceiling(max(a$x)), by = 1)
ydir <- seq(floor(min(a$y)), ceiling(max(a$y)), by = 1)
zdir <- seq(floor(min(a$z)), ceiling(max(a$z)), by = 1)

HH.grid <- expand.grid(x = xdir, y = ydir, z = zdir)
gridded(HH.grid) <- ~x + y + z
summary(HH.grid)




# Realizar la interpolación 
# Kriging simple: poner BC_C_CU ~ 1, beta = media_conocida
# Kriging Ordinario: poner BC_C_CU ~ 1, y no poner parametro beta
# Kriging Universal: poner BC_C_CU ~ x+y+z y no poner parametro beta
K <- krige(BC_C_CU ~ 1, a, HH.grid, v.fit.gau, nmax = 15)


############################################################
####################  plot (opcional)  #####################
############################################################

install.packages("rgl")
library(rgl)
K_df <- as.data.frame(K)
open3d()


plot3d(K_df$x, K_df$y, K_df$z, col = heat.colors(length(K_df$var1.pred))[rank(K_df$var1.pred)], size = 3)
title3d(main = "Predicciones del Kriging Simple", xlab = "X", ylab = "Y", zlab = "Z")


points3d(a$x, a$y, a$z, col = 'blue', size = 5)

open3d()


plot3d(K_df$x, K_df$y, K_df$z, col = heat.colors(length(K_df$var1.var))[rank(K_df$var1.var)], size = 3)
title3d(main = "Varianza de las Predicciones del Kriging Simple", xlab = "X", ylab = "Y", zlab = "Z")


points3d(a$x, a$y, a$z, col = 'blue', size = 5)

##################################################################
##################################################################
##################################################################

######################################################################
###################### Revertir trasnformacion y exportar ############
######################################################################

K_df <- as.data.frame(K)
if (lambda_optimo != 0) {
  K_df$CU_original <- ((lambda_optimo * K_df$var1.pred + 1)^(1/lambda_optimo))
} else {
  K_df$CU_original <- exp(K_df$var1.pred)
}

K_df$CU_original <- 100 - (K_df$CU_original * 100)
K_df$CU_original <- ifelse(K_df$CU_original < 0, 0, K_df$CU_original)


write.csv(K_df, "/Resultados/kriging_ordinario.csv",row.names = FALSE, col.names = FALSE)

#####################################################################
#####################################################################
#####################################################################

#####################################################################
###################### Kfolds Kriging  ########################
#####################################################################

#install.packages("caret")
library(sp)
library(gstat)
library(caret) 

K <- 10

folds <- createFolds(a$BC_C_CU, k = K, list = TRUE, returnTrain = TRUE)


errors <- list()

for (i in 1:K) {
 
  train_indices <- folds[[i]]
  test_indices <- setdiff(1:nrow(a), train_indices)
  
  train_data <- a[train_indices, ]
  test_data <- a[test_indices, ]
  
  bu = c(0.1, 0.5, seq(1,10,1), seq(12,40,2))
  # Kriging simple y ordinario: poner BC_C_CU ~ 1
  # Kriging Universal: poner BC_C_CU ~ x+y+z 
  v.fit.gau <- variogram(BC_C_CU ~ x+y+z, boundaries= bu,train_data, cressie= TRUE)
  v.fit.gau <- fit.variogram(v.fit.gau, model = vgm("Gau"))
  media_conocida <- mean(train_data$BC_C_CU, na.rm = TRUE)
  # Realizar la interpolación  en el conjunto de validacion
  # Kriging simple: poner BC_C_CU ~ 1, beta = media_conocida
  # Kriging Ordinario: poner BC_C_CU ~ 1, y no poner parametro beta
  # Kriging Universal: poner BC_C_CU ~ x+y+z y no poner parametro beta
  kriging_result <- krige(BC_C_CU ~ x+y+z, train_data, test_data, v.fit.gau, nmax = 15)
  
 
  predicted <- kriging_result$var1.pred
  actual <- test_data$BC_C_CU
  error <- actual - predicted

  errors[[i]] <- error
}


all_errors <- unlist(errors)

# Calcular métricas de error (RMSE y MAE)
rmse <- sqrt(mean(all_errors^2, na.rm = TRUE))
mae <- mean(abs(all_errors), na.rm = TRUE)


cat("Root Mean Squared Error (RMSE):", rmse, "\n")
cat("Mean Absolute Error (MAE):", mae, "\n")

















