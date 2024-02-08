# Biometrico 

## Install
```
npm i capacitor-native-biometric
```

## Biometrico | biometrico.tsx
```
import React, {useEffect, useState} from "react";
import {BiometryType, NativeBiometric} from "capacitor-native-biometric";
import {Preferences} from "@capacitor/preferences";
import {userServices} from "../services/user/user";
import {addUser} from "../store/slices/authSlice";
import {addUserEmp} from "../store/slices/authSliceEmp";
import {useAppDispatch} from "../store/hooks";

export const useBiometrico = ({switcher, renderLogin, setErrorMessage}) => {

    const {userLogin} = userServices();
    const dispatch = useAppDispatch();

    const [isAutenticado, setAutenticado] = useState(false);
    const [isBiometricoAvailability, setIsBiometricoAvailability] = useState(false);
    const [isFaceId, setIsFaceId] = useState(false);
    const [isFingerprint, setIsFingerprint] = useState(false);

    useEffect(() => {
        IsUserAndPassword().then(r => {
                if (r) {
                    setAutenticado(true);
                }
            }
        );

        checkBiometricAvailability().then((r) => {
            setIsBiometricoAvailability(r);
        });

    }, []);

    const checkBiometricAvailability = async () => {
        const resultado = await NativeBiometric.isAvailable();
        if (resultado.isAvailable) {
            setIsFaceId(resultado.biometryType === BiometryType.FACE_ID);
            setIsFingerprint(resultado.biometryType === BiometryType.FINGERPRINT);
            return true;
        }
        return false;
    };

    const performBiometricVerification = async () => {
        const resultado = await NativeBiometric.verifyIdentity({
            reason: "Para un inicio de sesión fácil",
            title: "Iniciar Sesión",
            subtitle: "Usa Huella Digital o Face ID para continuar",
            description: "Escoge tu método de autenticación preferido",
        }).then(() => true)
            .catch(() => false);
        if (resultado) {
            await checkUserAndPassword();
        }
    };

    const IsUserAndPassword = async () => {
        const {username, password} = await getUserAndPassword();
        return !(!username || !password);
    }


    const checkUserAndPassword = async () => {

        const {username, password} = await getUserAndPassword();

        const formData = {
            username: username,
            password: password,
        };

        let {status, statusText, data} = await userLogin(
            JSON.stringify(formData)
        );

        if (status == 200) {
            if (!Object.keys(data.result).includes("error")) {
                if (switcher === "urbanizaciones") {
                    let newUser = {
                        userId: data.result.user_id,
                        partnerId: data.result.partner_id,
                        name: data.result.name,
                        vat: data.result.vat,
                        telefono: data.result.telefono,
                        correo: Object.keys(data.result).includes("correo")
                            ? data.result.correo
                            : undefined,
                        rol: data.result.rol,
                        rolPersona: data.result.rol_persona,
                        image_1920: data.result.image_1920,
                        isLogin: data.result.isLogin,
                        rol_autorizacion: data.result.rol_autorizacion,
                        permission: data.result.permission,
                        session_token: undefined,
                        first_login: false,
                    };
                    dispatch(addUser(newUser));
                }
                if (switcher === "empresas") {
                    let newUser = {
                        userId: data.result.user_id,
                        partnerId: data.result.partner_id,
                        name: data.result.name,
                        vat: data.result.vat,
                        telefono: data.result.telefono,
                        correo: Object.keys(data.result).includes("correo")
                            ? data.result.correo
                            : undefined,
                        rol: data.result.rol,
                        image_1920: data.result.image_1920,
                        isLogin: data.result.isLogin,
                        permission: data.result.permission,
                        session_token: undefined,
                        first_login: false,
                    };
                    dispatch(addUserEmp(newUser));
                }
                renderLogin();
            } else {
                setErrorMessage(data.result.error);
            }
        } else {
            setErrorMessage(
                `Algo ha salido mal! Intente nuevamente más tarde. De ser posible, comunique este error al departamento de sistemas de Grupo Scanner Express. ${statusText}.`
            );
        }

    }

    const getUserAndPassword = async () => {
        const username = await Preferences.get({key: "username"});
        const password = await Preferences.get({key: "password"});
        return {username: username.value, password: password.value};
    };


    return {
        isAutenticado,
        isBiometricoAvailability,
        performBiometricVerification,
        setAutenticado,
    };
}
```


## Login Form
```
  const {
    isAutenticado,
    isBiometricoAvailability,
    performBiometricVerification,
    setAutenticado,
  } = useBiometrico({switcher, renderLogin, setErrorMessage});

<div className="container">
            <div className="line"></div>
            <div className="text">o ingresar con</div>
            <div className="line"></div>
          </div>

          {(!isBiometricoAvailability && isAutenticado) && (
              <IonButton
                  onClick={performBiometricVerification}
                  className="flex flex-col my-1 login"
              >
                Huella / Face ID
                {/*Icono de huella digital*/}
                <IonIcon slot="end" icon={fingerPrint}/>
              </IonButton>
          )}
          <IonText color="danger">{errorMessage}</IonText>
```
